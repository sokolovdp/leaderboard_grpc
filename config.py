import os
import logging

LOGGING_LEVEL = logging.DEBUG
LOGGING_FORMAT = "%(asctime)s,%(msecs)d %(levelname)s: %(message)s"
LOGGING_DATE_FORMAT = "%H:%M:%S"

MAX_WORKERS = 3
SERVER_PORT = '[::]:50051'

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
GAME_NAME = os.getenv('GAME_NAME', 'dimas')
PASSWORD_SALT = os.getenv('PASSWORD_HASH', 'quick fox jumps over the lazy dog')
LEADERBOARD_PAGE_SIZE = os.getenv('LEADERBOARD_PAGE_SIZE', 3)

LEADERBOARD_ALL_TIMES = GAME_NAME + 'leaderboard'
LEADERBOARD_TIMESTAMPS = GAME_NAME + '_timestamps'
LEADERBOARD_LAST_30_DAYS = GAME_NAME + '_last_30_days'

DEMO_LOGIN = os.getenv('DEMO_LOGIN', 'zz_top')
DEMO_PASSWORD = os.getenv('DEMO_PASSWORD', 'zz_top')
DEMO_MODE = os.getenv('DEMO_MODE', True)


