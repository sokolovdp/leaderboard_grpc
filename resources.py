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


def db_save_player_score(db, player_score):
    current_score = db.zscore(config.REDIS_LEADERBOARD, player_score.name)
    logger.info('player: %s old: %s new: %s' % (player_score.name, current_score, player_score.score))
    if not current_score or player_score.score > int(current_score):
        db.zadd(config.REDIS_LEADERBOARD, {player_score.name: player_score.score})
    rank = db.zrevrank(config.REDIS_LEADERBOARD, player_score.name) + 1
    return leaderboard_pb2.ScoreResponse(name=player_score.name, rank=rank)


def get_leaderboard(db, get_lb):
    leaderboard_count = db.zcount(config.REDIS_LEADERBOARD, '-inf', '+inf')
    max_page = (leaderboard_count + config.LEADERBOARD_PAGE_SIZE - 1) // config.LEADERBOARD_PAGE_SIZE
    if get_lb.page > max_page:
        return None, None, None
    page = get_lb.page - 1 if get_lb.page > 0 else 0  # pages numerated from 1
    start_rank = page * config.LEADERBOARD_PAGE_SIZE
    last_rank = start_rank + config.LEADERBOARD_PAGE_SIZE
    next_page = get_lb.page + 1 if last_rank < leaderboard_count else 0
    page_content = db.zrevrange(
        config.REDIS_LEADERBOARD,
        start_rank, last_rank,
        withscores=True,
        score_cast_func=int
    )
    leaderboard_page = [
        leaderboard_pb2.LeaderBoardRecord(name=name, score=score, rank=rank)
        for (name, score), rank in zip(page_content, range(start_rank+1, last_rank+1, 1))
    ]
    around_me_data = []
    if get_lb.name:
        pass
    return next_page, leaderboard_page, around_me_data
