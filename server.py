from concurrent import futures
import logging

import grpc

from proto import leaderboard_pb2
from proto import leaderboard_pb2_grpc
import resources


class LeaderBoardServicer(leaderboard_pb2_grpc.LeaderBoardServicer):
    """Provides methods that implement functionality of Leader Board server."""

    def __init__(self):
        self.db_connection = resources.setup_database()

    def AuthenticateUser(self, request, context):
        auth_token = resources.get_token(self.db_connection, request)
        return auth_token

    def RecordPlayerScore(self, request_iterator, context):
        for player_score in request_iterator:
            yield resources.store_player_score(self.db_connection, player_score)

    def GetLeaderBoard(self, request, context):
        next_page, results, around_me = resources.get_leaderboard(self.db_connection, request)
        leaderboard_response = leaderboard_pb2.LeaderBoardResponse()
        leaderboard_response.next_page = next_page
        leaderboard_response.results.extend(results)
        leaderboard_response.around_me.extend(around_me)
        return leaderboard_response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
    leaderboard_pb2_grpc.add_LeaderBoardServicer_to_server(LeaderBoardServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
