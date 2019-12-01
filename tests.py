import redis
from datetime import datetime

import config
import utils
import cron_job

initial_scores = [
    ('tuta', 10),
    ('sava', 20),
    ('kiki', 30),
    ('chupa', 40),
    ('old1', 200),
    ('old2', 300),
]


def preload_test_data(db: redis.Redis):
    db.flushall()  # clear all data
    db.hmset(
        name=f'{config.CLIENT_PREFIX}{config.DEMO_LOGIN}',
        mapping={
            'password': utils.hash_password(config.DEMO_PASSWORD),
            'token': utils.hash_password(config.DEMO_LOGIN + config.DEMO_PASSWORD)[:config.RPC_TOKEN_SIZE],
        }
    )
    for k, v in initial_scores[:4]:
        db.zadd(config.LEADERBOARD_ALL_TIMES, {k: v})
        db.zadd(config.LEADERBOARD_LAST_30_DAYS, {k: v})
        timestamp_now = datetime.timestamp(datetime.now())
        db.zadd(config.LEADERBOARD_TIMESTAMPS, {k: timestamp_now})

    today = datetime.now()
    today_timestamp = datetime.timestamp(datetime(year=today.year, month=today.month, day=today.day))
    timestamp_30_days_ago = today_timestamp - 2_592_000  # secs or 30 days ago
    for k, v in initial_scores[4:]:
        db.zadd(config.LEADERBOARD_ALL_TIMES, {k: v})
        db.zadd(config.LEADERBOARD_LAST_30_DAYS, {k: v})
        db.zadd(config.LEADERBOARD_TIMESTAMPS, {k: timestamp_30_days_ago})

    cron_job.update_monthly_table(db)


if __name__ == '__main__':
    preload_test_data(redis.Redis(host=config.REDIS_HOST))
