import json
from proto import leaderboard_pb2


def setup_database():
    return None


def get_token(db_connection, login_password):

    print(f'check credentials: {login_password.login} { login_password.password}')

    token = "super_secret_token_from_database"

    return token


def store_player_score(db_connection, player_score):

    print(f'store player score: {player_score.name} {player_score.score}')

    rank = 101

    return rank


def get_leaderboard(db_connection, get_lb):

    return 0, None, None

