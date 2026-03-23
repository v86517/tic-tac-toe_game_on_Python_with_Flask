from sqlalchemy import create_engine, or_, and_, desc
from sqlalchemy.orm import Session
import psycopg2

from src.config import DATABASE_URL
from src.datasource.model.ds_model import *

class Repository:
    def __init__(self):
        need_create_db = False
        need_create_tables = False
        try:
            connection = psycopg2.connect(user='postgres', password='postgres', host='127.0.0.1', port=5432)
        except Exception as e:
            print(f'{str(e)}')
            exit(1)
        else:
            cursor = connection.cursor()
            cursor.execute("SELECT 1 FROM pg_database WHERE datname='{dbname}'".format(dbname='tic_tac_toe'))

            if not cursor.fetchone():
                need_create_db = True
            cursor.close()
            connection.close()

        if need_create_db:
            connection = psycopg2.connect(database='postgres', user='postgres', password='postgres', host='127.0.0.1')
            connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

            # Создаем курсор для выполнения операций с базой данных
            cursor = connection.cursor()
            sql_create_database = "CREATE DATABASE tic_tac_toe"
            # Создаем базу данных
            cursor.execute(sql_create_database)
            # Закрываем соединение
            cursor.close()
            connection.close()
            need_create_tables = True


        self.engine = create_engine(DATABASE_URL)
        if need_create_tables:
            Base.metadata.create_all(self.engine)

    def get_ds_user_by_uuid_user(self, uuid_user):
        with Session(bind=self.engine) as session:
            result = session.query(UsersTable).filter(UsersTable.ds_user_uuid == uuid_user).first()
        return result

    def get_ds_user_by_login_user(self, login_user):
        with Session(bind=self.engine) as session:
            result = session.query(UsersTable).filter(UsersTable.ds_user_login == login_user).first()
        return result

    def add_ds_user(self, ds_user: UsersTable):
        result = False
        if self.get_ds_user_by_login_user(ds_user.ds_user_login) is None:
            with Session(bind=self.engine) as session:
                session.add(ds_user)
                session.commit()
                result = True
        return result

    def get_ds_board_by_uuid_game(self, uuid_game):
        with Session(bind=self.engine) as session:
            result = session.query(BoardsTable).filter(BoardsTable.ds_board_game_uuid == uuid_game).all()
        return result

    def get_started_ds_games_by_uuid_user(self, uuid_user):
        with Session(bind=self.engine) as session:
            result = session.query(GamesTable).filter(or_(
                and_(or_(GamesTable.ds_game_creator == uuid_user, GamesTable.ds_game_enemy == uuid_user),
                     GamesTable.ds_game_state.in_(["waiting players", "move X", "move O"])),
                and_(GamesTable.ds_game_two_players == True, GamesTable.ds_game_enemy == None,
                     GamesTable.ds_game_state == "waiting players"))
            ).all()
        return result

    def get_ds_game_by_uuid_game(self, uuid_game):
        with Session(bind=self.engine) as session:
            result = session.query(GamesTable).filter(GamesTable.ds_game_uuid == uuid_game).first()
        return result

    def add_ds_game(self, ds_game):
        with Session(bind=self.engine) as session:
            session.add(ds_game)
            session.commit()

    def add_ds_board(self, ds_board):
        with Session(bind=self.engine) as session:
            for cell in ds_board:
                session.add(cell)
            session.commit()

    def update_ds_game(self, ds_game: GamesTable):
        with Session(bind=self.engine) as session:
            elem = session.query(GamesTable).filter(GamesTable.ds_game_uuid == ds_game.ds_game_uuid).first()
            elem.ds_game_creator = ds_game.ds_game_creator
            elem.ds_game_creator_x_or_y = ds_game.ds_game_creator_x_or_y
            elem.ds_game_two_players = ds_game.ds_game_two_players
            elem.ds_game_enemy = ds_game.ds_game_enemy
            elem.ds_game_state = ds_game.ds_game_state

            session.add(elem)
            session.commit()

    def update_ds_board(self, ds_board):
        with Session(bind=self.engine) as session:
            for cell in ds_board:
                elem = session.query(BoardsTable).filter(
                and_(BoardsTable.ds_board_game_uuid == cell.ds_board_game_uuid, BoardsTable.ds_board_i == cell.ds_board_i,
                     BoardsTable.ds_board_j == cell.ds_board_j)).first()
                elem.ds_board_value = cell.ds_board_value
                session.add(elem)
            session.commit()

    def update_ds_user(self, ds_user: UsersTable):
        with Session(bind=self.engine) as session:
            elem = session.query(UsersTable).filter(UsersTable.ds_user_uuid == ds_user.ds_user_uuid).first()
            elem.ds_user_count_games = ds_user.ds_user_count_games
            elem.ds_user_count_wins = ds_user.ds_user_count_wins
            elem.ds_user_count_lose = ds_user.ds_user_count_lose
            elem.ds_user_count_draw = ds_user.ds_user_count_draw

            session.add(elem)
            session.commit()

    def get_finished_ds_games_by_uuid_user(self, uuid_user):
        with Session(bind=self.engine) as session:
            result = session.query(GamesTable).filter(
                and_(or_(GamesTable.ds_game_creator == uuid_user, GamesTable.ds_game_enemy == uuid_user),
                     GamesTable.ds_game_state.notin_(["waiting players", "move X", "move O"]))
            ).all()
        return result

    def get_ds_users_leaders_list(self, quantity):
        with Session(bind=self.engine) as session:
            result = session.query(UsersTable).order_by(desc(UsersTable.ds_user_count_wins), UsersTable.ds_user_count_lose).limit(
            quantity).all()
        return result
