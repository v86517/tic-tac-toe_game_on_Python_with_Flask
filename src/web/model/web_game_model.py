from src.config import CROSS, NOUGHT
from src.web.model.web_board_model import WebBoard
import uuid
import random
import datetime


class WebCurrentGame:
    def __init__(self, web_game_creator,
                 web_game_uuid=None,
                 web_game_board=None,
                 web_game_creator_x_or_y="not assigned",
                 web_game_two_players=False,
                 web_game_enemy=None,
                 web_game_state="waiting players",
                 web_game_datetime=None):
        self.web_game_creator = web_game_creator
        self.web_game_uuid = uuid.uuid4() if web_game_uuid is None else web_game_uuid
        self.web_game_board = WebBoard() if web_game_board is None else web_game_board
        self.web_game_creator_x_or_y = web_game_creator_x_or_y
        self.web_game_two_players = web_game_two_players
        self.web_game_enemy = web_game_enemy
        self.web_game_state = web_game_state
        if web_game_two_players == False and web_game_creator_x_or_y == "not assigned":
            self.web_game_creator_x_or_y = random.choice([CROSS, NOUGHT])
            self.web_game_state = "move X"
        self.web_game_datetime = datetime.datetime.now() if web_game_datetime is None else web_game_datetime