


root@99d6ecfc9c2c:/server# ps -ef | grep cron
root         7     1  0 11:03 ?        00:00:00 cron
root        20    14  0 11:04 pts/0    00:00:00 grep cron
root@99d6ecfc9c2c:/server# crontab -u root -l
0 3 * * * python3 /server/cron_job.py >> /var/log/cron.log 2>&1

