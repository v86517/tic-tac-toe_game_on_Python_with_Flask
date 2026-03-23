from src.config import BOARD_RANGE
from src.datasource.model.ds_model import UsersTable, GamesTable, BoardsTable
from src.domain.model.user_model import User
from src.domain.model.game_model import Game, GameState
from src.domain.model.board_model import Board
from src.datasource.repository.ds_repository import Repository


class DataMapper:
    def user_to_ds_user(user: User):
        result = UsersTable(
            ds_user_uuid=user.user_uuid,
            ds_user_login=user.user_login,
            ds_user_password=user.user_password,
            ds_user_count_games=user.user_count_games,
            ds_user_count_wins=user.user_count_wins,
            ds_user_count_lose=user.user_count_lose,
            ds_user_count_draw=user.user_count_draw)
        return result

    def board_to_ds_board(board: Board, uuid_game):
        result = []
        for i in range(BOARD_RANGE):
            for j in range(BOARD_RANGE):
                cell = BoardsTable(ds_board_game_uuid=uuid_game, ds_board_i=i, ds_board_j=j,
                                   ds_board_value=board.board[i][j])
                result.append(cell)
        return result

    def game_to_ds_game(game: Game):
        result = GamesTable(ds_game_uuid=game.game_uuid,
                            ds_game_creator=game.game_creator.user_uuid,
                            ds_game_creator_x_or_y=game.game_creator_x_or_o,
                            ds_game_two_players=game.game_two_players,
                            ds_game_enemy=game.game_enemy.user_uuid if game.game_enemy is not None else None,
                            ds_game_state=game.game_state.value,
                            ds_game_datetime=game.game_datetime)
        return result

    def game_to_ds_game_to_ds_field_to_ds_users(game: Game):
        result_game = DataMapper.game_to_ds_game(game)
        result_field = DataMapper.board_to_ds_board(game.game_board, game.game_uuid)
        result_creator = DataMapper.user_to_ds_user(game.game_creator)
        result_enemy = DataMapper.user_to_ds_user(game.game_enemy) if game.game_enemy is not None else None

        return result_game, result_field, result_creator, result_enemy

    def ds_user_to_user(ds_user: UsersTable):
        result = User(
            user_uuid=ds_user.ds_user_uuid,
            user_login=ds_user.ds_user_login,
            user_password=ds_user.ds_user_password,
            user_count_games=ds_user.ds_user_count_games,
            user_count_wins=ds_user.ds_user_count_wins,
            user_count_lose=ds_user.ds_user_count_lose,
            user_count_draw=ds_user.ds_user_count_draw)
        return result

    def ds_board_to_board(ds_board: BoardsTable):
        board = [[None] * BOARD_RANGE for _ in range(BOARD_RANGE)]
        for elem in ds_board:
            board[elem.ds_board_i][elem.ds_board_j] = elem.ds_board_value

        return Board(board)

    def ds_game_to_game(ds_game: GamesTable):
        repository = Repository()
        ds_user_creator = repository.get_ds_user_by_uuid_user(ds_game.ds_game_creator)
        ds_user_enemy = repository.get_ds_user_by_uuid_user(
            ds_game.ds_game_enemy) if ds_game.ds_game_enemy is not None else None
        ds_board = repository.get_ds_board_by_uuid_game(ds_game.ds_game_uuid)

        creator = DataMapper.ds_user_to_user(ds_user_creator)
        enemy = DataMapper.ds_user_to_user(ds_user_enemy) if ds_game.ds_game_enemy is not None else None
        board = DataMapper.ds_board_to_board(ds_board)

        result = Game(creator,
                      game_uuid=ds_game.ds_game_uuid,
                      game_board=board,
                      game_creator_x_or_o=ds_game.ds_game_creator_x_or_y,
                      game_two_players=ds_game.ds_game_two_players,
                      game_enemy=enemy,
                      game_state=GameState(ds_game.ds_game_state),
                      game_datetime=ds_game.ds_game_datetime)

        repository.engine.dispose()

        return result
