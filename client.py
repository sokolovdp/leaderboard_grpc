from base64 import b64encode

import grpc
from grpc_status import rpc_status
from google.rpc import code_pb2

from proto import leaderboard_pb2
from proto import leaderboard_pb2_grpc

import config
import resources

dummy_scores = [
    ('tuta', 12),
    ('sava', 35),
    ('kiki', 7),
    ('tuta', 12),
    ('sava', 50),
    ('kiki', 70),
    ('chupa', 65),
]


def get_auth_token(stub, login, password):
    credentials = leaderboard_pb2.BasicCredentials()
    credentials.data = b64encode(f'{login}:{password}'.encode('utf-8')).decode('utf-8')
    token_auth = stub.AuthenticateUser(credentials)
    return token_auth.token


def score_generator():
    for score in dummy_scores:
        yield leaderboard_pb2.PlayerScore(name=score[0], score=score[1])


def send_player_scores(stub, token_metadata):
    score_iterator = score_generator()
    try:
        player_ranks = stub.RecordPlayerScore(score_iterator, metadata=[token_metadata])
    except grpc.RpcError as rpc_error:
        resources.logger.error('gRPC error: %s' % str(rpc_error))
        status = rpc_status.from_call(rpc_error)
        if status.code == code_pb2.INVALID_ARGUMENT and status.message == 'page':
            resources.logger.error('invalid argument error')
        else:
            resources.logger.error('unexpected gRPC error: %s' % str(rpc_error))
        return []

    else:
        return player_ranks


def get_leaderboard_page(stub, token_metadata):
    try:
        get_lb = leaderboard_pb2.GetLeaderBoard()
        # get_lb.option = leaderboard_pb2.GetLeaderBoard.LAST_30_DAYS
        get_lb.option = leaderboard_pb2.GetLeaderBoard.ALL_TIME
        get_lb.page = 0
        get_lb.name = 'tuta'
        leaderboard_response = stub.GetLeaderBoardPages(get_lb, metadata=[token_metadata])
    except grpc.RpcError as rpc_error:
        status = rpc_status.from_call(rpc_error)
        if status.code == code_pb2.INVALID_ARGUMENT and status.message == 'page':
            resources.logger.error('page value exceeds max possible value')
        elif status.code == code_pb2.INVALID_ARGUMENT and status.message == 'name':
            resources.logger.error('player with such a name does not exist')
        else:
            resources.logger.error('unexpected gRPC error: %s' % str(rpc_error))
        return None
    else:
        return leaderboard_response


def run():
    with grpc.insecure_channel(config.SERVER_PORT) as channel:
        stub = leaderboard_pb2_grpc.LeaderBoardStub(channel)
        login = config.DEMO_LOGIN
        password = config.DEMO_PASSWORD
        token = get_auth_token(stub, login, password)
        if token:
            token_metadata = ('authorization', f'Bearer {token}')
            resources.logger.info('authorization token received')
        else:
            resources.logger.info('authorization failed for login: %s' % login)
            return

        player_ranks = send_player_scores(stub, token_metadata)

        for rank in player_ranks:
            resources.logger.info('player %s rank is %d' % (rank.name, rank.rank))

        result = get_leaderboard_page(stub, token_metadata)
        if result:
            print(result.next_page)
            print(result.results)
            print(result.around_me)


if __name__ == '__main__':
    run()
