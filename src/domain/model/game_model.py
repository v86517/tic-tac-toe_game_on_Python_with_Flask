from enum import Enum

from src.domain.model.board_model import *
import uuid
import random
import datetime


class GameState(Enum):
    WAITINGPLAYERS = "waiting players"
    MOVEX = "move X"
    MOVEO = "move O"
    WINX = "win X"
    WINO = "win O"
    DRAW = "draw"


class Game:
    def __init__(self,
                 game_creator,
                 game_uuid = None,
                 game_board = None,
                 game_creator_x_or_o = None,
                 game_two_players=False,
                 game_enemy = None,
                 game_state = GameState.WAITINGPLAYERS,
                 game_datetime = None):
        self.game_creator = game_creator
        self.game_uuid = uuid.uuid4() if game_uuid is None else game_uuid
        self.game_board = Board() if game_board is None else game_board
        self.game_creator_x_or_o = game_creator_x_or_o
        self.game_two_players = game_two_players
        self.game_enemy = game_enemy
        self.game_state = game_state
        if game_two_players == False and game_creator_x_or_o is None:
            self.game_creator_x_or_o = random.choice([CROSS, NOUGHT])
            self.game_state = GameState.MOVEX
        self.game_datetime = datetime.datetime.now() if game_datetime is None else game_datetime

    def change_turn(self):
        board_state = self.game_board.get_board_state()
        if board_state is None:
            if self.game_state == GameState.MOVEX:
                self.game_state = GameState.MOVEO
            elif self.game_state == GameState.MOVEO:
                self.game_state = GameState.MOVEX
        elif board_state == CROSS:
            self.game_state = GameState.WINX
        elif board_state == NOUGHT:
            self.game_state = GameState.WINO
        elif board_state == EMPTY:
            self.game_state = GameState.DRAW

    def get_next_move(self):
        if self.game_state == GameState.MOVEO:
            self.game_board.get_next_move(NOUGHT)
            self.change_turn()
        elif self.game_state == GameState.MOVEX:
            self.game_board.get_next_move(CROSS)
            self.change_turn()

    def get_game_state(self):
        return self.game_state.value

    def set_move(self, i, j):
        if self.game_state == GameState.MOVEO:
            self.game_board.make_move(i, j, NOUGHT)
            self.change_turn()
        elif self.game_state == GameState.MOVEX:
            self.game_board.make_move(i, j, CROSS)
            self.change_turn()

    def make_move(self, uuid_user, i, j):
        is_make_move = True

        whose_move_x_or_o = EMPTY
        if self.game_state == GameState.MOVEX:
            whose_move_x_or_o = CROSS
        elif self.game_state == GameState.MOVEO:
            whose_move_x_or_o = NOUGHT

        if self.game_creator.user_uuid == uuid_user:
            moving_user_x_or_o = self.game_creator_x_or_o
        else:
            moving_user_x_or_o = CROSS if self.game_creator_x_or_o == NOUGHT else NOUGHT

        if self.game_board.board[i][j] != EMPTY or whose_move_x_or_o != moving_user_x_or_o:
            is_make_move = False

        if is_make_move:
            self.set_move(i, j)
            if not self.game_two_players:
                self.get_next_move()


