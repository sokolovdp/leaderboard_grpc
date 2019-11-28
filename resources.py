import hashlib
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


def hash_password(password):
    salted = password + config.PASSWORD_SALT
    return hashlib.sha512(salted.encode("utf8")).hexdigest()


def db_connection():
    db = redis.Redis()
    db.set(f'LOGIN_{config.DEMO_LOGIN}', hash_password(config.DEMO_PASSWORD))  # store passwords
    db.zrem(config.REDIS_LEADERBOARD, 'kiki', 'sava', 'tuta', 'chupa')  # clear score list
    return db


def db_get_token(db, request):
    decoded_credentials = b64decode(request.data.encode('utf-8')).decode('utf-8')
    login, password = decoded_credentials.split(':')
    check = db.get(f'LOGIN_{login}')
    if hash_password(password) == check.decode('utf-8'):
        logger.info('login: %s credentials are valid' % login)
        token = "super_secret_token_from_database"
        return leaderboard_pb2.TokenAuth(token=token)
    else:
        logger.info('login: %s credentials are invalid!' % login)
        return leaderboard_pb2.TokenAuth(token='')


def db_save_player_score(db, request):
    current_score = db.zscore(config.REDIS_LEADERBOARD, request.name)
    logger.info('player: %s old: %s new: %s' % (request.name, current_score, request.score))
    if not current_score or request.score > int(current_score):
        db.zadd(config.REDIS_LEADERBOARD, {request.name: request.score})
    rank = db.zrevrank(config.REDIS_LEADERBOARD, request.name) + 1
    return leaderboard_pb2.ScoreResponse(name=request.name, rank=rank)


def player_in_leaderboard(leaderboard: list, name: str) -> bool:
    for record in leaderboard:
        if record.name == name:
            return True
    return False


def get_leaderboard_page(db, page: int) -> tuple:
    leaderboard_count = db.zcard(config.REDIS_LEADERBOARD)
    max_page = (leaderboard_count + config.LEADERBOARD_PAGE_SIZE - 1) // config.LEADERBOARD_PAGE_SIZE
    if page > max_page:
        raise ValueError('page')
    start_rank = page * config.LEADERBOARD_PAGE_SIZE
    last_rank = start_rank + config.LEADERBOARD_PAGE_SIZE
    next_page = page + 1 if last_rank < leaderboard_count else 0
    page_content = db.zrevrange(
        config.REDIS_LEADERBOARD,
        start_rank, last_rank,
        withscores=True,
        score_cast_func=int
    )
    leaderboard_data = [
        leaderboard_pb2.LeaderBoardRecord(name=name, score=score, rank=rank)
        for (name, score), rank in zip(page_content, range(start_rank+1, last_rank+1, 1))
    ]

    return leaderboard_data, next_page


def get_leaderboard(db, request):
    if request.option == leaderboard_pb2.GetLeaderBoard.STANDARD:
        leaderboard_page, next_page = get_leaderboard_page(db, request.page)
        around_me_data = []
        if request.name and not player_in_leaderboard(leaderboard_page, request.name):
            player_rank = db.zrevrank(config.REDIS_LEADERBOARD, request.name)
            if not player_rank:
                raise ValueError('name')
            player_page = (player_rank + config.LEADERBOARD_PAGE_SIZE - 1) // config.LEADERBOARD_PAGE_SIZE
            around_me_data, _ = get_leaderboard_page(db, player_page)
        return next_page, leaderboard_page, around_me_data
    elif request.option == leaderboard_pb2.GetLeaderBoard.ALL_TIME:
        return 100, [], []
    else:  # MONTHLY option
        return 200, [], []


