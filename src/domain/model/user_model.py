import uuid


class User:
    def __init__(self,
                 user_uuid = None,
                 user_login = "noname",
                 user_password = "password",
                 user_count_games = 0,
                 user_count_wins = 0,
                 user_count_lose = 0,
                 user_count_draw = 0):
        self.user_uuid = uuid.uuid4() if user_uuid is None else user_uuid
        self.user_login = user_login
        self.user_password = user_password
        self.user_count_games = user_count_games
        self.user_count_wins = user_count_wins
        self.user_count_lose = user_count_lose
        self.user_count_draw = user_count_draw