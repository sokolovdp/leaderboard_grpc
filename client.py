from base64 import b64encode
from http import HTTPStatus
from functools import wraps

import grpc
from grpc_status import rpc_status
from google.rpc import code_pb2

from proto.leaderboard_pb2 import BasicCredentials, PlayerScore, GetLeaderBoard
from proto.leaderboard_pb2_grpc import LeaderBoardStub

import config
from utils import logger

from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, exceptions  # get_jwt_identity

app = Flask(__name__)
app.rpc_token_metadata = None
app.config['JWT_SECRET_KEY'] = config.FLASK_JWT_SECRET_KEY
jwt = JWTManager(app)


@app.errorhandler(grpc.RpcError)
def grpc_server_error(rpc_error):
    app.rpc_token_metadata = None  # clear meta_data
    logger.error('gRPC error: %s' % str(rpc_error))
    err_name = rpc_error._state.code.name
    err_code = rpc_error._state.code.value[0]
    extended_status = rpc_status.from_call(rpc_error)
    return jsonify({'grpc_error': f'{err_name} {err_code} {extended_status}'}), HTTPStatus.CONFLICT


@app.errorhandler(Exception)
def internal_server_error(error):
    logger.error('flask internal error: %s' % str(error))
    return jsonify({'error': str(error)}), HTTPStatus.INTERNAL_SERVER_ERROR


def rpc_token_required(fn):
    """
    A decorator to check if rpc_token_metadata are present.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if app.rpc_token_metadata:
            return fn(*args, **kwargs)
        else:
            raise exceptions.NoAuthorizationError('RPC meta_token error')
    return wrapper


def get_rpc_auth_token(stub: LeaderBoardStub, username: str, password: str) -> str:
    credentials = BasicCredentials()
    credentials.data = b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')
    token_auth = stub.AuthenticateUser(credentials)
    return token_auth.token


@app.route('/auth', methods=['POST'])
def auth():
    username = request.authorization["username"]
    password = request.authorization["password"]
    with grpc.insecure_channel(config.GRPC_SERVER_PORT) as channel:
        stub = LeaderBoardStub(channel)
        token = get_rpc_auth_token(stub, username, password)
        if token:
            rpc_token_metadata = (config.AUTH_HEADER, f'{config.TOKEN_HEADER}{token}')
            app.rpc_token_metadata = rpc_token_metadata
            jwt_token = create_access_token(identity=username)
            logger.info('RPC authorization token received, JWT generated')
            return jsonify({'jwt': jwt_token}), HTTPStatus.OK
        else:
            return jsonify({'error': 'invalid credentials'}), HTTPStatus.UNAUTHORIZED


def verify_scores_format(score_list: list) -> list:
    if not score_list or not isinstance(score_list, list):
        raise TypeError
    verified_scores = []
    for name, score in score_list:
        if isinstance(name, str) and isinstance(score, int):
            verified_scores.append((name, score))
        else:
            raise TypeError
    return verified_scores


def score_generator(scores: list) -> PlayerScore:
    for score in scores:
        yield PlayerScore(name=score[0], score=score[1])


@app.route('/scores', methods=['POST', 'PUT'])
@jwt_required
@rpc_token_required
def set_scores():
    try:
        verified_scores = verify_scores_format(request.json)
    except TypeError:
        return jsonify({'error': 'invalid scores format'}), HTTPStatus.BAD_REQUEST

    score_iterator = score_generator(verified_scores)
    with grpc.insecure_channel(config.GRPC_SERVER_PORT) as channel:
        stub = LeaderBoardStub(channel)
        player_ranks = stub.RecordPlayerScore(score_iterator, metadata=[app.rpc_token_metadata])
        ranks = [(p.name, p.rank) for p in player_ranks]
    return jsonify(ranks), HTTPStatus.OK


@app.route('/leaderboard', methods=['GET'])
@jwt_required
@rpc_token_required
def leaderboard():
    last_30_days = 'last_30_days' in request.args
    name = request.args.get('name')
    try:
        page = int(request.args.get('page', 0))
    except ValueError:
        return jsonify({'error': 'page value must be int'}), HTTPStatus.BAD_REQUEST

    with grpc.insecure_channel(config.GRPC_SERVER_PORT) as channel:
        stub = LeaderBoardStub(channel)
        rpc_request = GetLeaderBoard()
        if last_30_days:
            rpc_request.option = GetLeaderBoard.LAST_30_DAYS
        if page:
            rpc_request.page = page
        if name:
            rpc_request.name = name
        try:
            leaderboard_response = stub.GetLeaderBoardPages(rpc_request, metadata=[app.rpc_token_metadata])
            results = [(r.name, r.score, r.rank) for r in leaderboard_response.results]
            around_me = [(a.name, a.score, a.rank) for a in leaderboard_response.around_me]
        except grpc.RpcError as rpc_error:
            status = rpc_status.from_call(rpc_error)
            if status.code == code_pb2.INVALID_ARGUMENT and status.message == 'page':
                error, status = 'page value exceeds max possible value', HTTPStatus.BAD_REQUEST
            elif status.code == code_pb2.INVALID_ARGUMENT and status.message == 'name':
                error, status = 'player with such a name does not exist', HTTPStatus.BAD_REQUEST
            else:
                raise rpc_error
            return jsonify({'error': error}), status
        else:
            return jsonify({
                'next_page': leaderboard_response.next_page,
                'results': results,
                'around_me': around_me
            }), HTTPStatus.OK


if __name__ == '__main__':
    app.run(host=config.FLASK_HOST, port=config.FLASK_PORT, debug=config.DEMO_MODE)
