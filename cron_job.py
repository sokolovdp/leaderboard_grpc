from datetime import datetime

import redis

import config
import resources


def update_monthly_table(db):
    today = datetime.now()
    today_timestamp = datetime.timestamp(datetime(year=today.year, month=today.month, day=today.day))
    timestamp_30_days_ago = today_timestamp - 2_592_000  # 60 * 60 * 24 * 30 secs ago
    with db.pipeline(transaction=True) as transaction:
        try:
            not_active_players = db.zrangebyscore(config.LEADERBOARD_TIMESTAMPS, 0, timestamp_30_days_ago)
            db.zrem(config.LEADERBOARD_LAST_30_DAYS, *not_active_players)
            transaction.execute()
        except Exception as e:
            resources.logger.error('cron job update_monthly_table results in error: %s' % str(e))
            print('cron job update_monthly_table results in error: %s' % str(e))
            exit(1)


if __name__ == '__main__':
    update_monthly_table(redis.Redis(host=config.REDIS_HOST))
