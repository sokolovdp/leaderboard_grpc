# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import leaderboard_pb2 as leaderboard__pb2


class LeaderBoardStub(object):
  """Interface exported by the server.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.AuthenticateUser = channel.unary_unary(
        '/leaderboard.LeaderBoard/AuthenticateUser',
        request_serializer=leaderboard__pb2.LoginPassword.SerializeToString,
        response_deserializer=leaderboard__pb2.Token.FromString,
        )
    self.RecordPlayerScore = channel.stream_stream(
        '/leaderboard.LeaderBoard/RecordPlayerScore',
        request_serializer=leaderboard__pb2.PlayerScore.SerializeToString,
        response_deserializer=leaderboard__pb2.ScoreResponse.FromString,
        )
    self.RouteChat = channel.unary_unary(
        '/leaderboard.LeaderBoard/RouteChat',
        request_serializer=leaderboard__pb2.GetLeaderBoard.SerializeToString,
        response_deserializer=leaderboard__pb2.LeaderBoardResponse.FromString,
        )


class LeaderBoardServicer(object):
  """Interface exported by the server.
  """

  def AuthenticateUser(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def RecordPlayerScore(self, request_iterator, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def RouteChat(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_LeaderBoardServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'AuthenticateUser': grpc.unary_unary_rpc_method_handler(
          servicer.AuthenticateUser,
          request_deserializer=leaderboard__pb2.LoginPassword.FromString,
          response_serializer=leaderboard__pb2.Token.SerializeToString,
      ),
      'RecordPlayerScore': grpc.stream_stream_rpc_method_handler(
          servicer.RecordPlayerScore,
          request_deserializer=leaderboard__pb2.PlayerScore.FromString,
          response_serializer=leaderboard__pb2.ScoreResponse.SerializeToString,
      ),
      'RouteChat': grpc.unary_unary_rpc_method_handler(
          servicer.RouteChat,
          request_deserializer=leaderboard__pb2.GetLeaderBoard.FromString,
          response_serializer=leaderboard__pb2.LeaderBoardResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'leaderboard.LeaderBoard', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
