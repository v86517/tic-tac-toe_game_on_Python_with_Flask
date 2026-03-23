from src.config import EMPTY, BOARD_RANGE


class WebBoard:
    def __init__(self, web_board = None):
        if web_board is None:
            self.web_board = [[EMPTY] * BOARD_RANGE for _ in range(BOARD_RANGE)]
        else:
            self.web_board = web_board
