import random
from proto import leaderboard_pb2
import logging

import config

logging.basicConfig(
    level=config.LOGGING_LEVEL,
    format=config.LOGGING_FORMAT,
    datefmt=config.LOGGING_DATE_FORMAT
)
logger = logging.getLogger('leaderboard')



def setup_database():
    return None


def get_token(db_connection, login_password):

    print(f'check credentials: {login_password.login} { login_password.password}')

    token = "super_secret_token_from_database"
    return leaderboard_pb2.TokenAuth(token=token)


def store_player_score(db_connection, player_score):

    print(f'store player score: {player_score.name} {player_score.score}')

    return leaderboard_pb2.ScoreResponse(name=player_score.name, rank=random.randint(1, 100))


def get_leaderboard(db_connection, get_lb):



    return 0, None, None

