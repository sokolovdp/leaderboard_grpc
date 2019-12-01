from concurrent import futures

import grpc
from grpc_status import rpc_status
from google.rpc import code_pb2, status_pb2

from proto import leaderboard_pb2
from proto import leaderboard_pb2_grpc

from rpc_server import database
from common import config
from common.utils import logger

INVALID_TOKEN_ERROR = 'invalid rpc token'
EXCEPTION_ARGS_ERROR = 'unexpected_value_error'


def create_internal_error_status(message):
    return status_pb2.Status(code=code_pb2.INTERNAL, message=message)


def create_invalid_argument_status(argument_name):
    return status_pb2.Status(code=code_pb2.INVALID_ARGUMENT, message=argument_name)


class LeaderBoardServicer(leaderboard_pb2_grpc.LeaderBoardServicer):
    """Provides methods that implement functionality of Leader Board server."""

    def __init__(self):
        self.db_connection = database.db_connection()
        self.token_validator = None

    def AuthenticateUser(self, request, context):
        auth_token = database.get_token(self.db_connection, request)
        if auth_token.token:  # if it's valid store value in validator
            self.token_validator.set_token(auth_token)
        return auth_token

    def RecordPlayerScore(self, request_iterator, context):
        try:
            for player_score in request_iterator:
                yield database.save_player_score(self.db_connection, player_score)
        except Exception as error:
            err_status = create_internal_error_status(str(error))
            context.abort_with_status(rpc_status.to_status(err_status))

    def GetLeaderBoardPages(self, request, context):
        try:
            leaderboard_response = database.get_leaderboard_data(self.db_connection, request)
        except ValueError as error:
            leaderboard_response = leaderboard_pb2.LeaderBoardResponse()
            argument_name = error.args[0] if error.args else EXCEPTION_ARGS_ERROR
            err_status = create_invalid_argument_status(argument_name)
            context.abort_with_status(rpc_status.to_status(err_status))

        return leaderboard_response


def unary_unary_rpc_terminator(code, details):
    def terminate(ignored_request, context):
        context.abort(code, details)

    return grpc.unary_unary_rpc_method_handler(terminate)


def stream_stream_rpc_terminator(code, details):
    def terminate(ignored_request, context):
        context.abort(code, details)

    return grpc.stream_stream_rpc_method_handler(terminate)


class AuthTokenValidatorInterceptor(grpc.ServerInterceptor):

    def __init__(self):
        self._auth_header_value = None

    def set_token(self, auth_token):
        self._auth_header_value = f'{config.TOKEN_HEADER}{auth_token.token}'

    def intercept_service(self, continuation, handler_call_details):
        meta_data = handler_call_details.invocation_metadata
        method = handler_call_details.method.rsplit('/', 1)[-1]
        if method == LeaderBoardServicer.AuthenticateUser.__name__:
            return continuation(handler_call_details)
        elif (config.AUTH_HEADER, self._auth_header_value) in meta_data:
            return continuation(handler_call_details)
        elif method == LeaderBoardServicer.RecordPlayerScore.__name__:
            return stream_stream_rpc_terminator(grpc.StatusCode.UNAUTHENTICATED, INVALID_TOKEN_ERROR)
        else:
            return unary_unary_rpc_terminator(grpc.StatusCode.UNAUTHENTICATED, INVALID_TOKEN_ERROR)


def serve():
    leaderboard_server = LeaderBoardServicer()
    leaderboard_server.token_validator = AuthTokenValidatorInterceptor()

    server = grpc.server(futures.ThreadPoolExecutor(
        max_workers=config.GRPC_SERVER_WORKERS),
        interceptors=(leaderboard_server.token_validator,)
    )
    leaderboard_pb2_grpc.add_LeaderBoardServicer_to_server(leaderboard_server, server)
    server.add_insecure_port(config.GRPC_SERVER_PORT)
    server.start()
    logger.info('gRPC leaderboard server started at port: %s' % config.GRPC_SERVER_PORT)
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
