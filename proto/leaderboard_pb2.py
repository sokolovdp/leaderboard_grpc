# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: leaderboard.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='leaderboard.proto',
  package='leaderboard',
  syntax='proto3',
  serialized_options=_b('\242\002\002LB'),
  serialized_pb=_b('\n\x11leaderboard.proto\x12\x0bleaderboard\"0\n\rLoginPassword\x12\r\n\x05login\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"\x1b\n\x05Token\x12\x12\n\nauth_token\x18\x01 \x01(\t\"M\n\x0bPlayerScore\x12!\n\x05token\x18\x01 \x01(\x0b\x32\x12.leaderboard.Token\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\r\n\x05score\x18\x03 \x01(\x03\"\x1d\n\rScoreResponse\x12\x0c\n\x04rank\x18\x01 \x01(\x03\"O\n\x0eGetLeaderBoard\x12!\n\x05token\x18\x01 \x01(\x0b\x32\x12.leaderboard.Token\x12\x0c\n\x04page\x18\x02 \x01(\x05\x12\x0c\n\x04name\x18\x03 \x01(\t\">\n\x11LeaderBoardRecord\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05score\x18\x02 \x01(\x03\x12\x0c\n\x04rank\x18\x03 \x01(\x05\"\x8c\x01\n\x13LeaderBoardResponse\x12/\n\x07results\x18\x01 \x03(\x0b\x32\x1e.leaderboard.LeaderBoardRecord\x12\x31\n\taround_me\x18\x02 \x03(\x0b\x32\x1e.leaderboard.LeaderBoardRecord\x12\x11\n\tnext_page\x18\x03 \x01(\x05\x32\xee\x01\n\x0bLeaderBoard\x12\x44\n\x10\x41uthenticateUser\x12\x1a.leaderboard.LoginPassword\x1a\x12.leaderboard.Token\"\x00\x12K\n\x11RecordPlayerScore\x12\x18.leaderboard.PlayerScore\x1a\x1a.leaderboard.ScoreResponse\"\x00\x12L\n\tRouteChat\x12\x1b.leaderboard.GetLeaderBoard\x1a .leaderboard.LeaderBoardResponse\"\x00\x42\x05\xa2\x02\x02LBb\x06proto3')
)




_LOGINPASSWORD = _descriptor.Descriptor(
  name='LoginPassword',
  full_name='leaderboard.LoginPassword',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='login', full_name='leaderboard.LoginPassword.login', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='password', full_name='leaderboard.LoginPassword.password', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=34,
  serialized_end=82,
)


_TOKEN = _descriptor.Descriptor(
  name='Token',
  full_name='leaderboard.Token',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='auth_token', full_name='leaderboard.Token.auth_token', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=84,
  serialized_end=111,
)


_PLAYERSCORE = _descriptor.Descriptor(
  name='PlayerScore',
  full_name='leaderboard.PlayerScore',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='token', full_name='leaderboard.PlayerScore.token', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='leaderboard.PlayerScore.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='score', full_name='leaderboard.PlayerScore.score', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=113,
  serialized_end=190,
)


_SCORERESPONSE = _descriptor.Descriptor(
  name='ScoreResponse',
  full_name='leaderboard.ScoreResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='rank', full_name='leaderboard.ScoreResponse.rank', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=192,
  serialized_end=221,
)


_GETLEADERBOARD = _descriptor.Descriptor(
  name='GetLeaderBoard',
  full_name='leaderboard.GetLeaderBoard',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='token', full_name='leaderboard.GetLeaderBoard.token', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='page', full_name='leaderboard.GetLeaderBoard.page', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='leaderboard.GetLeaderBoard.name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=223,
  serialized_end=302,
)


_LEADERBOARDRECORD = _descriptor.Descriptor(
  name='LeaderBoardRecord',
  full_name='leaderboard.LeaderBoardRecord',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='leaderboard.LeaderBoardRecord.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='score', full_name='leaderboard.LeaderBoardRecord.score', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='rank', full_name='leaderboard.LeaderBoardRecord.rank', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=304,
  serialized_end=366,
)


_LEADERBOARDRESPONSE = _descriptor.Descriptor(
  name='LeaderBoardResponse',
  full_name='leaderboard.LeaderBoardResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='results', full_name='leaderboard.LeaderBoardResponse.results', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='around_me', full_name='leaderboard.LeaderBoardResponse.around_me', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='next_page', full_name='leaderboard.LeaderBoardResponse.next_page', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=369,
  serialized_end=509,
)

_PLAYERSCORE.fields_by_name['token'].message_type = _TOKEN
_GETLEADERBOARD.fields_by_name['token'].message_type = _TOKEN
_LEADERBOARDRESPONSE.fields_by_name['results'].message_type = _LEADERBOARDRECORD
_LEADERBOARDRESPONSE.fields_by_name['around_me'].message_type = _LEADERBOARDRECORD
DESCRIPTOR.message_types_by_name['LoginPassword'] = _LOGINPASSWORD
DESCRIPTOR.message_types_by_name['Token'] = _TOKEN
DESCRIPTOR.message_types_by_name['PlayerScore'] = _PLAYERSCORE
DESCRIPTOR.message_types_by_name['ScoreResponse'] = _SCORERESPONSE
DESCRIPTOR.message_types_by_name['GetLeaderBoard'] = _GETLEADERBOARD
DESCRIPTOR.message_types_by_name['LeaderBoardRecord'] = _LEADERBOARDRECORD
DESCRIPTOR.message_types_by_name['LeaderBoardResponse'] = _LEADERBOARDRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

LoginPassword = _reflection.GeneratedProtocolMessageType('LoginPassword', (_message.Message,), {
  'DESCRIPTOR' : _LOGINPASSWORD,
  '__module__' : 'leaderboard_pb2'
  # @@protoc_insertion_point(class_scope:leaderboard.LoginPassword)
  })
_sym_db.RegisterMessage(LoginPassword)

Token = _reflection.GeneratedProtocolMessageType('Token', (_message.Message,), {
  'DESCRIPTOR' : _TOKEN,
  '__module__' : 'leaderboard_pb2'
  # @@protoc_insertion_point(class_scope:leaderboard.Token)
  })
_sym_db.RegisterMessage(Token)

PlayerScore = _reflection.GeneratedProtocolMessageType('PlayerScore', (_message.Message,), {
  'DESCRIPTOR' : _PLAYERSCORE,
  '__module__' : 'leaderboard_pb2'
  # @@protoc_insertion_point(class_scope:leaderboard.PlayerScore)
  })
_sym_db.RegisterMessage(PlayerScore)

ScoreResponse = _reflection.GeneratedProtocolMessageType('ScoreResponse', (_message.Message,), {
  'DESCRIPTOR' : _SCORERESPONSE,
  '__module__' : 'leaderboard_pb2'
  # @@protoc_insertion_point(class_scope:leaderboard.ScoreResponse)
  })
_sym_db.RegisterMessage(ScoreResponse)

GetLeaderBoard = _reflection.GeneratedProtocolMessageType('GetLeaderBoard', (_message.Message,), {
  'DESCRIPTOR' : _GETLEADERBOARD,
  '__module__' : 'leaderboard_pb2'
  # @@protoc_insertion_point(class_scope:leaderboard.GetLeaderBoard)
  })
_sym_db.RegisterMessage(GetLeaderBoard)

LeaderBoardRecord = _reflection.GeneratedProtocolMessageType('LeaderBoardRecord', (_message.Message,), {
  'DESCRIPTOR' : _LEADERBOARDRECORD,
  '__module__' : 'leaderboard_pb2'
  # @@protoc_insertion_point(class_scope:leaderboard.LeaderBoardRecord)
  })
_sym_db.RegisterMessage(LeaderBoardRecord)

LeaderBoardResponse = _reflection.GeneratedProtocolMessageType('LeaderBoardResponse', (_message.Message,), {
  'DESCRIPTOR' : _LEADERBOARDRESPONSE,
  '__module__' : 'leaderboard_pb2'
  # @@protoc_insertion_point(class_scope:leaderboard.LeaderBoardResponse)
  })
_sym_db.RegisterMessage(LeaderBoardResponse)


DESCRIPTOR._options = None

_LEADERBOARD = _descriptor.ServiceDescriptor(
  name='LeaderBoard',
  full_name='leaderboard.LeaderBoard',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=512,
  serialized_end=750,
  methods=[
  _descriptor.MethodDescriptor(
    name='AuthenticateUser',
    full_name='leaderboard.LeaderBoard.AuthenticateUser',
    index=0,
    containing_service=None,
    input_type=_LOGINPASSWORD,
    output_type=_TOKEN,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='RecordPlayerScore',
    full_name='leaderboard.LeaderBoard.RecordPlayerScore',
    index=1,
    containing_service=None,
    input_type=_PLAYERSCORE,
    output_type=_SCORERESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='RouteChat',
    full_name='leaderboard.LeaderBoard.RouteChat',
    index=2,
    containing_service=None,
    input_type=_GETLEADERBOARD,
    output_type=_LEADERBOARDRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_LEADERBOARD)

DESCRIPTOR.services_by_name['LeaderBoard'] = _LEADERBOARD

# @@protoc_insertion_point(module_scope)
