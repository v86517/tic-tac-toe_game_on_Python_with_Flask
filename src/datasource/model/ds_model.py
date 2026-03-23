from sqlalchemy.orm import declarative_base
from sqlalchemy import Integer, Column, ForeignKey, String, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID, BYTEA
Base = declarative_base()


class BoardsTable(Base):
    __tablename__ = 'boards_table'
    ds_board_id = Column(Integer, primary_key=True, autoincrement=True)
    ds_board_game_uuid = Column(UUID(as_uuid=True), ForeignKey('games_table.ds_game_uuid'), nullable=False)
    ds_board_i = Column(Integer, nullable=False)
    ds_board_j = Column(Integer, nullable=False)
    ds_board_value = Column(String(1), nullable=False)


class GamesTable(Base):
    __tablename__ = 'games_table'
    ds_game_uuid = Column(UUID(as_uuid=True), primary_key=True)
    ds_game_creator = Column(UUID(as_uuid=True), ForeignKey('users_table.ds_user_uuid'), nullable=False)
    ds_game_creator_x_or_y = Column(String(1))
    ds_game_two_players = Column(Boolean, nullable=False)
    ds_game_enemy = Column(UUID(as_uuid=True), ForeignKey('users_table.ds_user_uuid'), nullable=True)
    ds_game_state = Column(String(100), nullable=False)
    ds_game_datetime = Column(DateTime, nullable=False)


class UsersTable(Base):
    __tablename__ = 'users_table'
    ds_user_uuid = Column(UUID(as_uuid=True), primary_key=True)
    ds_user_login = Column(String(100), nullable=False)
    ds_user_password = Column(BYTEA(), nullable=False)
    ds_user_count_games = Column(Integer, nullable=False)
    ds_user_count_wins = Column(Integer, nullable=False)
    ds_user_count_lose = Column(Integer, nullable=False)
    ds_user_count_draw = Column(Integer, nullable=False)
