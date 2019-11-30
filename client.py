from base64 import b64encode
from http import HTTPStatus

import grpc
from grpc_status import rpc_status
from google.rpc import code_pb2

from proto import leaderboard_pb2
from proto import leaderboard_pb2_grpc

import config
from utils import logger

from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token  # get_jwt_identity

app = Flask(__name__)
app.rpc_token_metadata = None
app.config['JWT_SECRET_KEY'] = config.FLASK_JWT_SECRET_KEY
jwt = JWTManager(app)


def get_rpc_auth_token(stub, username, password):
    credentials = leaderboard_pb2.BasicCredentials()
    credentials.data = b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')
    token_auth = stub.AuthenticateUser(credentials)
    return token_auth.token


@app.route('/auth', methods=['POST'])
def auth():
    username = request.authorization["username"]
    password = request.authorization["password"]
    with grpc.insecure_channel(config.GRPC_SERVER_PORT) as channel:
        stub = leaderboard_pb2_grpc.LeaderBoardStub(channel)
        token = get_rpc_auth_token(stub, username, password)
    if token:
        rpc_token_metadata = ('authorization', f'Bearer {token}')
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


def score_generator(scores):
    for score in scores:
        yield leaderboard_pb2.PlayerScore(name=score[0], score=score[1])


@app.route('/scores', methods=['POST', 'PUT'])
@jwt_required
def set_scores():  # TODO META_DATA CHECK
    try:
        verified_scores = verify_scores_format(request.json)
    except TypeError:
        return jsonify({'error': 'invalid scores format'}), HTTPStatus.BAD_REQUEST

    score_iterator = score_generator(verified_scores)
    try:
        with grpc.insecure_channel(config.GRPC_SERVER_PORT) as channel:
            stub = leaderboard_pb2_grpc.LeaderBoardStub(channel)
            player_ranks = stub.RecordPlayerScore(score_iterator, metadata=[app.rpc_token_metadata])
            ranks = [(p.name, p.rank) for p in player_ranks]
    except grpc.RpcError as rpc_error:
        logger.error('gRPC error: %s' % str(rpc_error))
        status = rpc_status.from_call(rpc_error)
        return jsonify({'error': status}), HTTPStatus.CONFLICT
    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    else:
        return jsonify(ranks), HTTPStatus.OK


@app.route('/leaderboard', methods=['GET'])
@jwt_required
def leaderboard():  # TODO META_DATA CHECK
    last_30_days = 'last_30_days' in request.args
    name = request.args.get('name')
    try:
        page = int(request.args.get('page', 0))
    except ValueError:
        return jsonify({'error': 'page value must be int'}), HTTPStatus.BAD_REQUEST

    with grpc.insecure_channel(config.GRPC_SERVER_PORT) as channel:
        stub = leaderboard_pb2_grpc.LeaderBoardStub(channel)
        rpc_request = leaderboard_pb2.GetLeaderBoard()
        if last_30_days:
            rpc_request.option = leaderboard_pb2.GetLeaderBoard.LAST_30_DAYS
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
                error, status = 'unexpected gRPC error: %s' % str(rpc_error), HTTPStatus.INTERNAL_SERVER_ERROR
            logger.error(error)
            return jsonify({'error': error}), status
        except Exception as e:
            return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
        else:
            return jsonify({
                'next_page': leaderboard_response.next_page,
                'results': results,
                'around_me': around_me
            }), HTTPStatus.OK


if __name__ == '__main__':
    app.run(host=config.FLASK_HOST, port=config.FLASK_PORT, debug=config.DEMO_MODE)
