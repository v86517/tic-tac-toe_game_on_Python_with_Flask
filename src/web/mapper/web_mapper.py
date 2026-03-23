from src.config import CROSS, NOUGHT, EMPTY
from src.web.model.web_user_model import WebUser
from src.web.model.web_game_model import WebCurrentGame
from src.web.model.web_board_model import WebBoard
from src.domain.model.user_model import User
from src.domain.model.game_model import Game, GameState
from src.domain.model.board_model import Board


class WebMapper:
    def user_to_web_user(user: User):
        result = WebUser()
        result.web_user_uuid = user.user_uuid
        result.web_user_login = user.user_login
        result.web_user_password = user.user_password
        result.web_user_count_games = user.user_count_games
        result.web_user_count_wins = user.user_count_wins
        result.web_user_count_lose = user.user_count_lose
        result.web_user_count_draw = user.user_count_draw
        return result

    def board_to_web_board(board: Board):
        new_board = []

        for line in board.board:
            new_line = []
            for cell in line:
                new_line.append(cell)
            new_board.append(new_line)

        return WebBoard(new_board)

    def game_to_web_game(game: Game):
        creator = WebMapper.user_to_web_user(game.game_creator)
        board = WebMapper.board_to_web_board(game.game_board)
        type_creator = "not assigned"
        if game.game_creator_x_or_o == CROSS:
            type_creator = CROSS
        elif game.game_creator_x_or_o == NOUGHT:
            type_creator = NOUGHT
        enemy = None if game.game_enemy is None else WebMapper.user_to_web_user(game.game_enemy)

        result = WebCurrentGame(creator,
                                web_game_uuid=game.game_uuid,
                                web_game_board=board,
                                web_game_creator_x_or_y=type_creator,
                                web_game_two_players=game.game_two_players,
                                web_game_enemy=enemy,
                                web_game_state=game.game_state.value,
                                web_game_datetime=game.game_datetime)
        return result

    def web_user_to_user(web_user: WebUser):
        result = User(
            user_uuid=web_user.web_user_uuid,
            user_login=web_user.web_user_login,
            user_password=web_user.web_user_password,
            user_count_games=web_user.web_user_count_games,
            user_count_wins=web_user.web_user_count_wins,
            user_count_lose=web_user.web_user_count_lose,
            user_count_draw=web_user.web_user_count_draw)
        return result

    def web_board_to_board(web_board: WebBoard):
        new_web_board = []

        for line in web_board.web_board:
            new_line = []
            for cell in line:
                new_line.append(cell)
            new_web_board.append(new_line)

        return WebBoard(new_web_board)

    def web_game_to_game(web_game: WebCurrentGame):
        game_creator = WebMapper.web_user_to_user(web_game.web_game_creator)
        game_board = WebMapper.web_board_to_board(web_game.web_game_board)
        game_creator_x_or_o = EMPTY
        if web_game.web_game_creator_x_or_y == CROSS:
            game_creator_x_or_o = CROSS
        elif web_game.web_game_creator_x_or_y == NOUGHT:
            game_creator_x_or_o = NOUGHT
        game_enemy = None if web_game.web_game_enemy is None else WebMapper.web_user_to_user(web_game.web_game_enemy)

        result = Game(game_creator,
                      game_uuid=web_game.web_game_uuid,
                      game_board=game_board,
                      game_creator_x_or_o=game_creator_x_or_o,
                      game_two_players=web_game.web_game_two_players,
                      game_enemy=game_enemy,
                      game_state=GameState(web_game.web_game_state),
                      game_datetime=web_game.web_game_datetime)
        return result
