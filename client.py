from base64 import b64encode

import grpc
from grpc_status import rpc_status
from google.rpc import code_pb2

from proto import leaderboard_pb2
from proto import leaderboard_pb2_grpc

import config
from utils import logger

from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

app = Flask(__name__)
app.rpc_token_metadata = None
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)

dummy_scores = [
    ('tuta', 12),
    ('sava', 50),
    ('kiki', 70),
    ('chupa', 65),
]


def get_auth_token(stub, username, password):
    credentials = leaderboard_pb2.BasicCredentials()
    credentials.data = b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')
    token_auth = stub.AuthenticateUser(credentials)
    return token_auth.token


@app.route('/auth', methods=['POST'])
def auth():
    username = request.authorization["username"]
    password = request.authorization["password"]
    with grpc.insecure_channel(config.SERVER_PORT) as channel:
        stub = leaderboard_pb2_grpc.LeaderBoardStub(channel)
        token = get_auth_token(stub, username, password)
    if token:
        rpc_token_metadata = ('authorization', f'Bearer {token}')
        app.rpc_token_metadata = rpc_token_metadata
        jwt_token = create_access_token(identity=username)
        logger.info('RPC authorization token received, JWT generated')
        return jsonify({'jwt': jwt_token}), 200
    else:
        return jsonify({'error': 'invalid credentials'}), 401


def score_generator():
    for score in dummy_scores:
        yield leaderboard_pb2.PlayerScore(name=score[0], score=score[1])


@app.route('/scores', methods=['POST', 'PUT'])
@jwt_required
def set_scores():
    args = request.json
    score_iterator = score_generator()
    try:
        with grpc.insecure_channel(config.SERVER_PORT) as channel:
            stub = leaderboard_pb2_grpc.LeaderBoardStub(channel)
            player_ranks = stub.RecordPlayerScore(score_iterator, metadata=[app.rpc_token_metadata])
            ranks = [(p.name, p.rank) for p in player_ranks]
    except grpc.RpcError as rpc_error:
        logger.error('gRPC error: %s' % str(rpc_error))
        status = rpc_status.from_call(rpc_error)
        if status.code == code_pb2.INVALID_ARGUMENT and status.message == 'page':
            error = 'invalid argument error'
        else:
            error = 'unexpected gRPC error: %s' % str(rpc_error)
        logger.error(error)
        return jsonify({'error': error}), 400
    else:
        return jsonify(ranks), 200


def get_leaderboard_page(stub, token_metadata):
    try:
        get_lb = leaderboard_pb2.GetLeaderBoard()
        get_lb.option = leaderboard_pb2.GetLeaderBoard.LAST_30_DAYS
        # get_lb.option = leaderboard_pb2.GetLeaderBoard.ALL_TIME
        get_lb.page = 0
        get_lb.name = 'tuta'
        leaderboard_response = stub.GetLeaderBoardPages(get_lb, metadata=[token_metadata])
    except grpc.RpcError as rpc_error:
        status = rpc_status.from_call(rpc_error)
        if status.code == code_pb2.INVALID_ARGUMENT and status.message == 'page':
            logger.error('page value exceeds max possible value')
        elif status.code == code_pb2.INVALID_ARGUMENT and status.message == 'name':
            logger.error('player with such a name does not exist')
        else:
            logger.error('unexpected gRPC error: %s' % str(rpc_error))
        return None
    else:
        return leaderboard_response


@app.route('/leaderboard', methods=['GET'])
@jwt_required
def leaderboard():
    args = request.args
    with grpc.insecure_channel(config.SERVER_PORT) as channel:
        stub = leaderboard_pb2_grpc.LeaderBoardStub(channel)
        get_lb = leaderboard_pb2.GetLeaderBoard()
        # get_lb.option = leaderboard_pb2.GetLeaderBoard.LAST_30_DAYS
        get_lb.page = 0
        get_lb.name = 'kiki'
        leaderboard_response = stub.GetLeaderBoardPages(get_lb, metadata=[app.rpc_token_metadata])

        results = [(r.name, r.score, r.rank) for r in leaderboard_response.results]
        around_me = [(a.name, a.score, a.rank) for a in leaderboard_response.around_me]
        return {
            'next_page': leaderboard_response.next_page,
            'results': results,
            'around_me': around_me
            }


if __name__ == '__main__':
    app.run(debug=True)   # host=, port=
