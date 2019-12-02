import os
import logging

LOGGING_LEVEL = logging.DEBUG
LOGGING_FORMAT = "%(asctime)s,%(msecs)d %(levelname)s: %(message)s"
LOGGING_DATE_FORMAT = "%H:%M:%S"

GRPC_SERVER_WORKERS = os.getenv('GRPC_SERVER_WORKERS', 2)
GRPC_SERVER_PORT = os.getenv('GRPC_SERVER_PORT', '0.0.0.0:50051')
GRPC_SERVER_HOST = os.getenv('GRPC_SERVER_HOST', GRPC_SERVER_PORT)
AUTH_HEADER = 'authorization'
TOKEN_HEADER = 'Bearer '
RPC_TOKEN_SIZE = 7

PASSWORD_SALT = os.getenv('PASSWORD_HASH', 'Quick brown fox jumps over the lazy dog')
LEADERBOARD_PAGE_SIZE = os.getenv('LEADERBOARD_PAGE_SIZE', 3)
REDIS_HOST = os.getenv('REDIS_HOST', '0.0.0.0')
CLIENT_PREFIX = 'RPCLIENT_'

LEADERBOARD_GAME_NAME = os.getenv('GAME_NAME', 'dimas')
LEADERBOARD_ALL_TIMES = LEADERBOARD_GAME_NAME + 'leaderboard'
LEADERBOARD_TIMESTAMPS = LEADERBOARD_GAME_NAME + '_timestamps'
LEADERBOARD_LAST_30_DAYS = LEADERBOARD_GAME_NAME + '_last_30_days'

DEMO_LOGIN = os.getenv('DEMO_LOGIN', 'zz_top')
DEMO_PASSWORD = os.getenv('DEMO_PASSWORD', 'zz_top')
DEMO_MODE = os.getenv('DEMO_MODE', True)

FLASK_JWT_SECRET_KEY = os.getenv('FLASK_JWT_SECRET_KEY', 'flask_jwt_secret_key')
FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
FLASK_PORT = os.getenv('FLASK_PORT', 5000)
