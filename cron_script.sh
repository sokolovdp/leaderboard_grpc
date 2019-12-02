touch /var/spool/cron/leaderboard
/usr/bin/crontab /var/spool/cron/leaderboard
echo "0 3 * * * cd /home/dmitrii/leaderboard_grpc && cron_job.py >> ~/cron.log" >> /var/spool/cron/leaderboard