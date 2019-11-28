import os
import logging

LOGGING_LEVEL = logging.DEBUG
LOGGING_FORMAT = "%(asctime)s,%(msecs)d %(levelname)s: %(message)s"
LOGGING_DATE_FORMAT = "%H:%M:%S"

MAX_WORKERS = 3
SERVER_PORT = '[::]:50051'

REDIS_HOST = ''
REDIS_LEADERBOARD = 'leaderboard'
REDIS_TIMESTAMPS = REDIS_LEADERBOARD + '_timestamps'

PASSWORD_SALT = os.getenv('PASSWORD_HASH', 'quick fox jumps over the lazy dog')

DEMO_LOGIN = os.getenv('DEMO_LOGIN', 'zz_top')
DEMO_PASSWORD = os.getenv('DEMO_PASSWORD', 'zz_top')

LEADERBOARD_PAGE_SIZE = os.getenv('LEADERBOARD_PAGE_SIZE', 3)
