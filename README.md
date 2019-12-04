# Demo project of API based gRPC for Python framework with Rest API based on Flask framework as a gateway.

gRPC server implements a leaderboard API for games. gRPC client is used to test the API. The client communicates with the server only via ​gRPC, but the client is also accessible by Rest API.

## Functionality
The gRPC server is capable of doing the following things:
- Authentication
- Storing player’s score
- Getting the all time leaderboard, or last 30 days leaderboard

## Authentication 
User authentication implemented in two points: 
- Rest API (external) authentication uses Basic and JWT token authorizations with 30 minutes lifetime.
- gRPC API (internal) authentication uses Token schema with short token (default length 7 bytes) without time limit.

## Leaderboards implementation
Redis database is used to store player scores. There are 3 sorted sets (Z sets) to store player scores data:
- timestamps - keeps player score timestamp
- all_time_leaderboard - keeps player's scores
- last_30_days_leaderboard - keeps player's scores which where received during last 30 days

## Storing player’s score
In order to store a player's score, a stream connection is opened to the gRPC server.
The request consists of player name and score (integer). If such player does not exist in the database, it has to be created. If a
player with such name already exists, the score for this player is updated if the
score​ passed to the API​ is larger​ than the one stored in the database. The response returns player’s position within the leaderboard.



## API's points
```text
​ POST /categories/
```
```text
 GET /categories/<id>/​
```

##  Implementation notes
API using recursive SQL queries returns both all ancestors (parents) and all descendants (children) of an element, plus its siblings (categories with the same parent)

## Unit tests
```text
python manage.py test

```

## Postman collection with API tests
https://www.getpostman.com/collections/ea2dfb57228b08319c7c








root@99d6ecfc9c2c:/server# ps -ef | grep cron
root         7     1  0 11:03 ?        00:00:00 cron
root        20    14  0 11:04 pts/0    00:00:00 grep cron
root@99d6ecfc9c2c:/server# crontab -u root -l
0 3 * * * python3 /server/cron_job.py >> /var/log/cron.log 2>&1

