import logging

import grpc

from proto import leaderboard_pb2
from proto import leaderboard_pb2_grpc


dummy_scores = [
    ('tuta', 12),
    ('sava', 35),
    ('kiki', 7)
]


def get_auth_token(stub, login, password):
    credentials = leaderboard_pb2.LoginPassword()
    credentials.login = login
    credentials.password = password
    token_auth = stub.AuthenticateUser(credentials)
    return token_auth.token


def score_generator():
    for score in dummy_scores:
        yield leaderboard_pb2.PlayerScore(name=score[0], score=score[1])


def send_player_scores(stub):
    score_iterator = score_generator()
    player_ranks = stub.RecordPlayerScore(score_iterator)
    return player_ranks


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = leaderboard_pb2_grpc.LeaderBoardStub(channel)

        print("-------------- Get Token --------------")
        token = get_auth_token(stub, "dmitrii", "sokol1959")
        print(f'Auth_token: "{token}"')

        print("-------------- Send Player Scores --------------")
        player_ranks = send_player_scores(stub)
        for rank in player_ranks:
            print(f'player {rank.name} rank is {rank.rank}')
        #
        # print("-------------- Get Leader Board --------------")
        # guide_record_route(stub)


if __name__ == '__main__':
    logging.basicConfig()
    run()
