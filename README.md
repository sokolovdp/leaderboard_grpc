# Demo Leaderboard project of API based on gRPC Python framework with Rest API as a gateway.
gRPC server implements a leaderboard API for games. Server communicates with gRPC client. The client communicates with the server only via ​gRPC, but it is also receive and sends player scores and ranking information via traditional Rest API.

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
- **timestamps** - keeps player score timestamp
- **all_time_leaderboard** - keeps player's scores
- **last_30_days_leaderboard** - keeps player's scores which where received during last 30 days

## Storing player’s score
In order to store a player's score, a stream connection will be opened to the gRPC server.
The request consists of player name and score (integer). If such player does not exist in the database, it has to be created. If a
player with such name already exists, the score for this player will be updated if the
score​ passed to the API​ is larger​ than the one stored in the database. The response returns player’s position within the leaderboard.

## Getting the leaderboard
The leaderboard request consists of player’s name (optional) and page number and option to see the alltime/monthly leaderboard. Each request to the leaderboard should return one page of
results. One page should consist of configured number of results (key 'results').
If the name of the player passed, and the player is not in this list of results (and their result
is not in any of the previous pages), a list of players around the current player will be
returned (key 'around_me'). Each object of a player has to contain their name, score and position (rank).
Plus response has next page value (key 'next_page')

## External Rest API's points
```text
​ POST /auth
```
if Basic auth credentials are valid, returns JWT value
```text
 GET /leaderboard?name=<player_name>&page=<int>&last_30_days=<0 or 1>
```
send leaderboard data in JSON format
```text
 POST /scores
```
receives list of player's scores in JSON format

##  Implementation notes
 - Redis Z-set provides ranking functionality, so no ranking calculations implemented within the server code
 - It is recommended to use Self-Balanced Order-Statistic Tree (SBOST), with a hash table to implement the same functionality for SQL database (like Postgres, or Oracle), see the [link](https://www.hindawi.com/journals/ijcgt/2018/3234873/)
 - Scheduled cron job (python3 /server/cron_job.py) is used to remove scores older than 30 days from the corresponding set.


## Testing
No unit tests implemented, but for testing purpose during initialization database preloaded with the following player's scores:
```python
initial_scores = [
    ('tuta', 10),
    ('sava', 20),
    ('kiki', 30),
    ('chupa', 40),
    ('old1', 200),   # <- time stamps older than 30 days ago
    ('old2', 300),
]
```
Load [Postman collection](https://www.getpostman.com/collections/6ced8f0d843f04a4635c) with preconfigured data to run API tests

## Run application using Docker containers
There are 3 docker's containers:
- Redis database
- gRPC server
- gRPC client with Rest API gateway

To run application: download repo and run **docker-compose up** command inside **leaderboard_grpc** folder

After successful star-up the following messages should appear in the console:
```text
...
server    | 15:25:28,206 INFO: from monthly table removed: old1, old2
server    | 15:25:28,242 INFO: gRPC leaderboard server started at port: 0.0.0.0:50051
...
client    | 15:25:29,471 INFO: GRPC server address: server:50051
...
client    | 15:25:29,477 INFO:  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)

```
