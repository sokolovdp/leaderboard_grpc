import random
import logging
from base64 import b64decode

import redis

from proto import leaderboard_pb2
import config

logging.basicConfig(
    level=config.LOGGING_LEVEL,
    format=config.LOGGING_FORMAT,
    datefmt=config.LOGGING_DATE_FORMAT
)
logger = logging.getLogger('leaderboard')


logins = [

]


def db_connection():
    db = redis.Redis()
    # init DB with test data
    db.set(f'LOGIN_dmitrii', 'sokol1959')  #

    return db


def db_get_token(db, request):
    decoded_credentials = b64decode(request.data.encode('utf-8')).decode('utf-8')
    login, password = decoded_credentials.split(':')
    check = db.get(f'LOGIN_{login}')
    if password == check.decode('utf-8'):
        logger.info('login: %s credentials are valid' % login)
        token = "super_secret_token_from_database"
        return leaderboard_pb2.TokenAuth(token=token)
    else:
        logger.info('login: %s credentials are invalid!' % login)
        return leaderboard_pb2.TokenAuth(token='')


def db_save_player_score(db_connection, player_score):
    print(f'store player score: {player_score.name} {player_score.score}')

    return leaderboard_pb2.ScoreResponse(name=player_score.name, rank=random.randint(1, 100))


def get_leaderboard(db_connection, get_lb):
    return 0, None, None
