from datetime import datetime

import redis

from common import config
from common.utils import logger


def remove_old_records_from_monthly_table(db):
    today = datetime.now()
    today_timestamp = datetime.timestamp(datetime(year=today.year, month=today.month, day=today.day))
    timestamp_30_days_ago = today_timestamp - 2_592_000  # secs or 30 days ago
    with db.pipeline(transaction=True) as transaction:
        try:
            not_active_players = db.zrangebyscore(config.LEADERBOARD_TIMESTAMPS, 0, timestamp_30_days_ago)
            db.zrem(config.LEADERBOARD_LAST_30_DAYS, *not_active_players)
            transaction.execute()
        except Exception as e:
            logger.error('remove_old_records_from_monthly_table proc results in error: %s' % str(e))
            exit(1)
    logger.info('from monthly table removed: %s' % ', '.join(not_active_players))


if __name__ == '__main__':
    logger.error('cron job update_monthly_table started')
    remove_old_records_from_monthly_table(redis.Redis(host=config.REDIS_HOST))
    logger.error('cron job update_monthly_table finished')

