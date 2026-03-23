from src.config import NOUGHT, CROSS, LEADERS_QTY
from src.datasource.repository.ds_repository import Repository
from src.domain.model.game_model import Game
from src.domain.service.interface_service import InterfaceService
from src.datasource.mapper.ds_mapper import DataMapper
import random


class Service(InterfaceService):
    def __init__(self, repository: Repository):
        self.repository = repository

    def create_game(self, uuid_user, two_players):
        ds_user = self.repository.get_ds_user_by_uuid_user(uuid_user)
        user = DataMapper.ds_user_to_user(ds_user)
        game = Game(user, game_two_players=two_players)
        user.user_count_games += 1

        if game.game_creator_x_or_o == NOUGHT:
            game.get_next_move()

        ds_game, ds_board, ds_user_creator, ds_user_enemy = DataMapper.game_to_ds_game_to_ds_field_to_ds_users(game)
        self.repository.add_ds_game(ds_game)
        self.repository.add_ds_board(ds_board)
        self.repository.update_ds_user(ds_user_creator)

        return game.game_uuid

    def get_game(self, uuid_game):
        ds_game = self.repository.get_ds_game_by_uuid_game(uuid_game)
        result = DataMapper.ds_game_to_game(ds_game)
        return result

    def get_game_state(self, uuid_game):
        game = self.get_game(uuid_game)
        return game.get_game_state()

    def make_move(self, uuid_user, uuid_game, i, j):
        game = self.get_game(uuid_game)
        game.make_move(uuid_user, i, j)

        ds_game, ds_board, ds_user_creator, ds_user_enemy = DataMapper.game_to_ds_game_to_ds_field_to_ds_users(game)
        self.repository.update_ds_game(ds_game)
        self.repository.update_ds_board(ds_board)
        self.repository.update_ds_user(ds_user_creator)
        if ds_user_enemy is not None:
            self.repository.update_ds_user(ds_user_enemy)

    def get_started_ds_games_by_uuid_user(self, uuid_user):
        result = []
        list_ds_games = self.repository.get_started_ds_games_by_uuid_user(uuid_user)

        for ds_game in list_ds_games:
            creator_login = self.repository.get_ds_user_by_uuid_user(ds_game.ds_game_creator)
            result.append({"creator_login": creator_login.ds_user_login,
                           "creator": ds_game.ds_game_creator,
                           "uuid_game": ds_game.ds_game_uuid,
                           "created_datetime": ds_game.ds_game_datetime})
        return result

    def join_to_game(self, uuid_user, uuid_game):
        result = False

        ds_game = self.repository.get_ds_game_by_uuid_game(uuid_game)

        if ds_game is not None:
            if ds_game.ds_game_creator == uuid_user or (ds_game.ds_game_enemy is not None and ds_game.ds_game_enemy == uuid_user):
                result = True
            elif ds_game.ds_game_enemy is None:
                result = True
                ds_game.ds_game_enemy = uuid_user
                ds_game.ds_game_creator_x_or_y = random.choice([CROSS, NOUGHT])
                ds_game.ds_game_state = "move X"
                self.repository.update_ds_game(ds_game)
                ds_user = self.repository.get_ds_user_by_uuid_user(uuid_user)
                ds_user.ds_user_count_games += 1
                self.repository.update_ds_user(ds_user)

        return result

    def get_user(self, uuid_user):
        ds_user = self.repository.get_ds_user_by_uuid_user(uuid_user)
        user = DataMapper.ds_user_to_user(ds_user) if ds_user is not None else None
        return user

    def get_finished_ds_games_by_uuid_user(self, uuid_user):
        result = []
        ds_games = self.repository.get_finished_ds_games_by_uuid_user(uuid_user)

        for ds_game in ds_games:
            if ds_game.ds_game_creator == uuid_user:
                ds_game_creator_x_or_y = ds_game.ds_game_creator_x_or_y
            else:
                ds_game_creator_x_or_y = CROSS if ds_game.ds_game_creator_x_or_y == NOUGHT else NOUGHT

            creator_x_or_y = ds_game_creator_x_or_y

            result.append({"id_game": ds_game.ds_game_uuid,
                           "icon_user": creator_x_or_y,
                           "status_game": ds_game.ds_game_state,
                           "created_datetime": ds_game.ds_game_datetime})
        return result

    def get_ds_users_leaders_list(self):
        result = []
        ds_users_leaders_list = self.repository.get_ds_users_leaders_list(LEADERS_QTY)

        for ds_user in ds_users_leaders_list:
            result.append({"id_user": ds_user.ds_user_uuid,
                           "login": ds_user.ds_user_login,
                           "count_wins": ds_user.ds_user_count_wins,
                           "count_lose": ds_user.ds_user_count_lose,
                           "count_draw": ds_user.ds_user_count_draw})
        return result

    def add_count_wins(self, uuid_user):
        ds_user = self.repository.get_ds_user_by_uuid_user(uuid_user)
        ds_user.ds_user_count_wins += 1
        self.repository.update_ds_user(ds_user)

    def add_count_lose(self, uuid_user):
        ds_user = self.repository.get_ds_user_by_uuid_user(uuid_user)
        ds_user.ds_user_count_lose += 1
        self.repository.update_ds_user(ds_user)

    def add_count_draw(self, uuid_user):
        ds_user = self.repository.get_ds_user_by_uuid_user(uuid_user)
        ds_user.ds_user_count_draw += 1
        self.repository.update_ds_user(ds_user)