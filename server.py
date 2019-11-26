from concurrent import futures

import grpc

from proto import leaderboard_pb2
from proto import leaderboard_pb2_grpc

import resources
import config

token_validator = None


class LeaderBoardServicer(leaderboard_pb2_grpc.LeaderBoardServicer):
    """Provides methods that implement functionality of Leader Board server."""

    def __init__(self):
        self.db_connection = resources.db_connection()

    def AuthenticateUser(self, request, context):
        auth_token = resources.db_get_token(self.db_connection, request)
        if auth_token.token:  # if it's valid store value in validator
            token_validator.set_token(auth_token)
        return auth_token

    def RecordPlayerScore(self, request_iterator, context):
        for player_score in request_iterator:
            yield resources.db_save_player_score(self.db_connection, player_score)

    def GetLeaderBoard(self, request, context):
        next_page, results, around_me = resources.get_leaderboard(self.db_connection, request)
        leaderboard_response = leaderboard_pb2.LeaderBoardResponse()
        leaderboard_response.next_page = next_page
        leaderboard_response.results.extend(results)
        leaderboard_response.around_me.extend(around_me)
        return leaderboard_response


def _unary_unary_rpc_terminator(code, details):
    def terminate(ignored_request, context):
        context.abort(code, details)

    return grpc.unary_unary_rpc_method_handler(terminate)


def _stream_stream_rpc_terminator(code, details):
    def terminate(ignored_request, context):
        context.abort(code, details)

    return grpc.stream_stream_rpc_method_handler(terminate)


class AuthTokenValidatorInterceptor(grpc.ServerInterceptor):

    def __init__(self, *args, **kwargs):
        self._header = 'authorization'
        self._value = None
        self.code = grpc.StatusCode.UNAUTHENTICATED
        self.details = 'Invalid token!'

    def set_token(self, auth_token):
        self._value = f'Bearer {auth_token.token}'

    def intercept_service(self, continuation, handler_call_details):
        meta_data = handler_call_details.invocation_metadata
        method = handler_call_details.method.rsplit('/', 1)[-1]
        if method == LeaderBoardServicer.AuthenticateUser.__name__:
            return continuation(handler_call_details)
        elif (self._header, self._value) in meta_data:
            return continuation(handler_call_details)
        elif method == LeaderBoardServicer.RecordPlayerScore.__name__:
            return _stream_stream_rpc_terminator(self.code, self.details)
        else:
            return _unary_unary_rpc_terminator(self.code, self.details)


def serve():
    global token_validator

    token_validator = AuthTokenValidatorInterceptor()

    server = grpc.server(futures.ThreadPoolExecutor(
        max_workers=config.MAX_WORKERS),
        interceptors=(token_validator, )
    )
    leaderboard_pb2_grpc.add_LeaderBoardServicer_to_server(LeaderBoardServicer(), server)
    server.add_insecure_port(config.SERVER_PORT)
    server.start()
    resources.logger.info('leaderboard started at: %s workers: %d' % (config.SERVER_PORT, config.MAX_WORKERS))
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
