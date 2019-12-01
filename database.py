from base64 import b64decode
from datetime import datetime

import redis
from redis import Redis

from proto.leaderboard_pb2 import (
    BasicCredentials,
    TokenAuth,
    PlayerScore,
    ScoreResponse,
    LeaderBoardRecord,
    GetLeaderBoard,
    LeaderBoardResponse,
)

import config
from utils import logger, hash_password


def initialize_database(db: Redis):
    if config.DEMO_MODE:
        import tests
        tests.preload_test_data(db)


def db_connection() -> Redis:
    db = redis.StrictRedis(host=config.REDIS_HOST, port=6379, charset="utf-8", decode_responses=True)
    initialize_database(db)
    return db


def get_token(db: Redis, request: BasicCredentials) -> TokenAuth:
    rcvd_credentials = b64decode(request.data.encode('utf-8')).decode('utf-8')
    username, password = rcvd_credentials.split(':')
    db_credentials = db.hgetall(f'{config.CLIENT_PREFIX}{username}')
    if db_credentials and hash_password(password) == db_credentials['password']:
        logger.info('username: %s credentials are valid' % username)
        rpc_token = db_credentials['token']
        return TokenAuth(token=rpc_token)
    else:
        logger.error('username: %s credentials are invalid!' % username)
        return TokenAuth(token='')


def store_score_in_table(db: Redis, table_name: str, request: PlayerScore) -> int:
    current_score = db.zscore(table_name, request.name)
    if not current_score or request.score > int(current_score):
        db.zadd(table_name, {request.name: request.score})
    return current_score


def save_player_score(db: Redis, request: PlayerScore) -> ScoreResponse:
    timestamp = datetime.timestamp(datetime.now())
    with db.pipeline(transaction=True) as transaction:
        try:
            current_score = store_score_in_table(db, config.LEADERBOARD_ALL_TIMES, request)
            _ = store_score_in_table(db, config.LEADERBOARD_LAST_30_DAYS, request)
            rank = db.zrevrank(config.LEADERBOARD_ALL_TIMES, request.name) + 1
            db.zadd(config.LEADERBOARD_TIMESTAMPS, {request.name: timestamp})
            transaction.execute()
        except Exception as e:
            raise e
    logger.info('player: %s old: %s new: %s' % (request.name, current_score, request.score))
    return ScoreResponse(name=request.name, rank=rank)


def player_score_in_page(name: str, result_page: list) -> bool:
    for record in result_page:
        if record.name == name:
            return True
    return False


def get_db_data(db: Redis, table_name: str, start_rank: int, last_rank: int) -> list:
    db_data = db.zrevrange(
        table_name,
        start_rank,
        last_rank,
        withscores=True,
        score_cast_func=int
    )
    db_data_ranked = [
        LeaderBoardRecord(name=name, score=score, rank=rank)
        for (name, score), rank in zip(db_data, range(start_rank + 1, last_rank + 1, 1))
    ]
    return db_data_ranked


def get_leaderboard_page(db: Redis, table_name: str, page: int) -> list:
    start_rank = page * config.LEADERBOARD_PAGE_SIZE
    last_rank = start_rank + config.LEADERBOARD_PAGE_SIZE
    leaderboard_data = get_db_data(db, table_name, start_rank, last_rank)
    return leaderboard_data


def calculate_next_page(db: Redis, table_name: str, page: int) -> int:
    max_page = (db.zcard(table_name) + config.LEADERBOARD_PAGE_SIZE - 1) // config.LEADERBOARD_PAGE_SIZE
    if page >= max_page:  # raise error: invalid page value
        raise ValueError('page')
    return page + 1 % max_page


def calculate_player_page(rank):
    return ((rank + config.LEADERBOARD_PAGE_SIZE - 1) // config.LEADERBOARD_PAGE_SIZE) - 1


def get_results(db: Redis, table_name: str, request: GetLeaderBoard) -> LeaderBoardResponse:
    next_page = calculate_next_page(db, table_name, request.page)
    results_page = get_leaderboard_page(db, table_name, request.page)
    around_me_page = []
    if request.name and not player_score_in_page(request.name, results_page):
        player_rank = db.zrevrank(table_name, request.name)
        if not player_rank:  # raise error: invalid player name
            raise ValueError('name')
        player_page = calculate_player_page(player_rank)
        around_me_page = get_leaderboard_page(db, table_name, player_page)
    leaderboard_response = LeaderBoardResponse()
    leaderboard_response.next_page = next_page
    leaderboard_response.results.extend(results_page)
    leaderboard_response.around_me.extend(around_me_page)
    return leaderboard_response


def get_leaderboard_data(db: Redis, request: GetLeaderBoard) -> tuple:
    if request.option == GetLeaderBoard.ALL_TIME:
        return get_results(db, config.LEADERBOARD_ALL_TIMES, request)
    else:
        return get_results(db, config.LEADERBOARD_LAST_30_DAYS, request)
