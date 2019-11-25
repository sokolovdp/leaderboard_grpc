from collections import defaultdict, namedtuple

from proto import leaderboard_pb2

my_leader_board = defaultdict(tuple)
Score = namedtuple('Score', ['score', 'rank'])


def setup_database():
    return None


def get_token(db_connection, login_password):

    print(f'check credentials: {login_password.login} { login_password.password}')

    token = "super_secret_token_from_database"
    return leaderboard_pb2.TokenAuth(token=token)


def store_player_score(db_connection, player_score):
    global my_leader_board

    print(f'store player score: {player_score.name} {player_score.score}')



    my_leader_board.append((player_score.name, player_score))
    my_leader_board.sort(key=lambda x: x[1])
    rank = my_leader_board.index()

    return leaderboard_pb2.ScoreResponse(name=player_score.name, rank=rank)


def get_leaderboard(db_connection, get_lb):



    return 0, None, None

