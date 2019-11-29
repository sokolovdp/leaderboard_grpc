import hashlib
import logging
from base64 import b64decode
from datetime import datetime

import redis

from proto import leaderboard_pb2

import config

logging.basicConfig(
    level=config.LOGGING_LEVEL,
    format=config.LOGGING_FORMAT,
    datefmt=config.LOGGING_DATE_FORMAT
)
logger = logging.getLogger('leaderboard')


def initialize_database(db):
    db.set(f'LOGIN_{config.DEMO_LOGIN}', hash_password(config.DEMO_PASSWORD))  # store passwords
    db.zrem(config.LEADERBOARD_ALL_TIMES, 'kiki', 'sava', 'tuta', 'chupa')  # clear score list


def hash_password(password):
    salted = password + config.PASSWORD_SALT
    return hashlib.sha512(salted.encode("utf8")).hexdigest()


def db_connection():
    db = redis.Redis(host=config.REDIS_HOST)
    initialize_database(db)
    return db


def db_get_token(db, request):
    decoded_credentials = b64decode(request.data.encode('utf-8')).decode('utf-8')
    login, password = decoded_credentials.split(':')
    check = db.get(f'LOGIN_{login}')
    if check and hash_password(password) == check.decode('utf-8'):
        logger.info('login: %s credentials are valid' % login)
        token = "super_secret_token_from_database"
        return leaderboard_pb2.TokenAuth(token=token)
    else:
        logger.info('login: %s credentials are invalid!' % login)
        return leaderboard_pb2.TokenAuth(token='')


def db_save_player_score(db, request):
    current_score = db.zscore(config.LEADERBOARD_ALL_TIMES, request.name)
    logger.info('player: %s old: %s new: %s' % (request.name, current_score, request.score))
    if not current_score or request.score > int(current_score):
        db.zadd(config.LEADERBOARD_ALL_TIMES, {request.name: request.score})
    rank = db.zrevrank(config.LEADERBOARD_ALL_TIMES, request.name) + 1
    timestamp = datetime.timestamp(datetime.now())
    db.zadd(config.LEADERBOARD_TIMESTAMPS, {request.name: timestamp})
    return leaderboard_pb2.ScoreResponse(name=request.name, rank=rank)


def player_in_leaderboard(leaderboard: list, name: str) -> bool:
    for record in leaderboard:
        if record.name == name:
            return True
    return False


def get_db_data(db, table_name, start_rank, last_rank):
    db_data = db.zrevrange(
        table_name,
        start_rank,
        last_rank,
        withscores=True,
        score_cast_func=int
    )
    db_data_ranked = [
        leaderboard_pb2.LeaderBoardRecord(name=name, score=score, rank=rank)
        for (name, score), rank in zip(db_data, range(start_rank + 1, last_rank + 1, 1))
    ]
    return db_data_ranked


def get_leaderboard_page(db, table_name, page: int) -> tuple:
    leaderboard_count = db.zcard(table_name)
    max_page = (leaderboard_count + config.LEADERBOARD_PAGE_SIZE - 1) // config.LEADERBOARD_PAGE_SIZE
    if page > max_page:
        raise ValueError('page')
    start_rank = page * config.LEADERBOARD_PAGE_SIZE
    last_rank = start_rank + config.LEADERBOARD_PAGE_SIZE
    next_page = page + 1 if last_rank < leaderboard_count else 0
    leaderboard_data = get_db_data(db, table_name, start_rank, last_rank)
    return leaderboard_data, next_page


def get_leaderboard_from_table(db, table_name, request):
    leaderboard_page, next_page = get_leaderboard_page(db, table_name, request.page)
    around_me_data = []
    # check if player's name was given, and his result is in resulting page, if not then find its page
    if request.name and not player_in_leaderboard(leaderboard_page, request.name):
        player_rank = db.zrevrank(table_name, request.name)
        if not player_rank:
            raise ValueError('name')
        player_page = (player_rank + config.LEADERBOARD_PAGE_SIZE - 1) // config.LEADERBOARD_PAGE_SIZE
        around_me_data, _ = get_leaderboard_page(db, table_name, player_page)
    return next_page, leaderboard_page, around_me_data


def db_get_leaderboard_data(db, request):
    if request.option == leaderboard_pb2.GetLeaderBoard.ALL_TIME:
        return get_leaderboard_from_table(db, config.LEADERBOARD_ALL_TIMES, request)
    else:
        return 100, [], []
        # return get_leaderboard_from_table(db, config.LEADERBOARD_LAST_30_DAYS, request)





