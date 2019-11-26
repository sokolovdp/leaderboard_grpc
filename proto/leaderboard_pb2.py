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
  serialized_options=None,
  serialized_pb=_b('\n\x11leaderboard.proto\x12\x0bleaderboard\" \n\x10\x42\x61sicCredentials\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\t\"\x1a\n\tTokenAuth\x12\r\n\x05token\x18\x01 \x01(\t\"*\n\x0bPlayerScore\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05score\x18\x02 \x01(\r\"+\n\rScoreResponse\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04rank\x18\x02 \x01(\r\"#\n\x05GetLB\x12\x0c\n\x04page\x18\x01 \x01(\r\x12\x0c\n\x04name\x18\x02 \x01(\t\">\n\x11LeaderBoardRecord\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05score\x18\x02 \x01(\r\x12\x0c\n\x04rank\x18\x03 \x01(\r\"\x8c\x01\n\x13LeaderBoardResponse\x12/\n\x07results\x18\x01 \x03(\x0b\x32\x1e.leaderboard.LeaderBoardRecord\x12\x31\n\taround_me\x18\x02 \x03(\x0b\x32\x1e.leaderboard.LeaderBoardRecord\x12\x11\n\tnext_page\x18\x03 \x01(\r2\xf5\x01\n\x0bLeaderBoard\x12K\n\x10\x41uthenticateUser\x12\x1d.leaderboard.BasicCredentials\x1a\x16.leaderboard.TokenAuth\"\x00\x12O\n\x11RecordPlayerScore\x12\x18.leaderboard.PlayerScore\x1a\x1a.leaderboard.ScoreResponse\"\x00(\x01\x30\x01\x12H\n\x0eGetLeaderBoard\x12\x12.leaderboard.GetLB\x1a .leaderboard.LeaderBoardResponse\"\x00\x62\x06proto3')
)




_BASICCREDENTIALS = _descriptor.Descriptor(
  name='BasicCredentials',
  full_name='leaderboard.BasicCredentials',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='leaderboard.BasicCredentials.data', index=0,
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
  serialized_start=34,
  serialized_end=66,
)


_TOKENAUTH = _descriptor.Descriptor(
  name='TokenAuth',
  full_name='leaderboard.TokenAuth',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='token', full_name='leaderboard.TokenAuth.token', index=0,
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
  serialized_start=68,
  serialized_end=94,
)


_PLAYERSCORE = _descriptor.Descriptor(
  name='PlayerScore',
  full_name='leaderboard.PlayerScore',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='leaderboard.PlayerScore.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='score', full_name='leaderboard.PlayerScore.score', index=1,
      number=2, type=13, cpp_type=3, label=1,
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
  serialized_start=96,
  serialized_end=138,
)


_SCORERESPONSE = _descriptor.Descriptor(
  name='ScoreResponse',
  full_name='leaderboard.ScoreResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='leaderboard.ScoreResponse.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='rank', full_name='leaderboard.ScoreResponse.rank', index=1,
      number=2, type=13, cpp_type=3, label=1,
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
  serialized_start=140,
  serialized_end=183,
)


_GETLB = _descriptor.Descriptor(
  name='GetLB',
  full_name='leaderboard.GetLB',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='page', full_name='leaderboard.GetLB.page', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='leaderboard.GetLB.name', index=1,
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
  serialized_start=185,
  serialized_end=220,
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
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='rank', full_name='leaderboard.LeaderBoardRecord.rank', index=2,
      number=3, type=13, cpp_type=3, label=1,
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
  serialized_start=222,
  serialized_end=284,
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
      number=3, type=13, cpp_type=3, label=1,
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
  serialized_start=287,
  serialized_end=427,
)

_LEADERBOARDRESPONSE.fields_by_name['results'].message_type = _LEADERBOARDRECORD
_LEADERBOARDRESPONSE.fields_by_name['around_me'].message_type = _LEADERBOARDRECORD
DESCRIPTOR.message_types_by_name['BasicCredentials'] = _BASICCREDENTIALS
DESCRIPTOR.message_types_by_name['TokenAuth'] = _TOKENAUTH
DESCRIPTOR.message_types_by_name['PlayerScore'] = _PLAYERSCORE
DESCRIPTOR.message_types_by_name['ScoreResponse'] = _SCORERESPONSE
DESCRIPTOR.message_types_by_name['GetLB'] = _GETLB
DESCRIPTOR.message_types_by_name['LeaderBoardRecord'] = _LEADERBOARDRECORD
DESCRIPTOR.message_types_by_name['LeaderBoardResponse'] = _LEADERBOARDRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

BasicCredentials = _reflection.GeneratedProtocolMessageType('BasicCredentials', (_message.Message,), {
  'DESCRIPTOR' : _BASICCREDENTIALS,
  '__module__' : 'leaderboard_pb2'
  # @@protoc_insertion_point(class_scope:leaderboard.BasicCredentials)
  })
_sym_db.RegisterMessage(BasicCredentials)

TokenAuth = _reflection.GeneratedProtocolMessageType('TokenAuth', (_message.Message,), {
  'DESCRIPTOR' : _TOKENAUTH,
  '__module__' : 'leaderboard_pb2'
  # @@protoc_insertion_point(class_scope:leaderboard.TokenAuth)
  })
_sym_db.RegisterMessage(TokenAuth)

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

GetLB = _reflection.GeneratedProtocolMessageType('GetLB', (_message.Message,), {
  'DESCRIPTOR' : _GETLB,
  '__module__' : 'leaderboard_pb2'
  # @@protoc_insertion_point(class_scope:leaderboard.GetLB)
  })
_sym_db.RegisterMessage(GetLB)

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



_LEADERBOARD = _descriptor.ServiceDescriptor(
  name='LeaderBoard',
  full_name='leaderboard.LeaderBoard',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=430,
  serialized_end=675,
  methods=[
  _descriptor.MethodDescriptor(
    name='AuthenticateUser',
    full_name='leaderboard.LeaderBoard.AuthenticateUser',
    index=0,
    containing_service=None,
    input_type=_BASICCREDENTIALS,
    output_type=_TOKENAUTH,
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
    name='GetLeaderBoard',
    full_name='leaderboard.LeaderBoard.GetLeaderBoard',
    index=2,
    containing_service=None,
    input_type=_GETLB,
    output_type=_LEADERBOARDRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_LEADERBOARD)

DESCRIPTOR.services_by_name['LeaderBoard'] = _LEADERBOARD

# @@protoc_insertion_point(module_scope)
