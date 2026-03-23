from src.config import EMPTY, CROSS, NOUGHT, BOARD_RANGE

class Board:
    def __init__(self, board=None):
        if board is None:
            self.board = [[EMPTY] * BOARD_RANGE for _ in range(BOARD_RANGE)]
        else:
            self.board = board

    def check_winner(self):
        # check rows
        for row in  range(BOARD_RANGE):
            for col in  range(BOARD_RANGE):
                if self.board[row][0] != self.board[row][col]:
                    break
                if col == (BOARD_RANGE - 1) and self.board[row][0] != EMPTY:
                    return self.board[row][0]

        # check columns
        for row in range(BOARD_RANGE):
            for col in range(BOARD_RANGE):
                if self.board[0][row] != self.board[col][row]:
                    break
                if col == (BOARD_RANGE - 1) and self.board[0][row] is not EMPTY:
                    return self.board[0][row]

        # check diagonal \
        for i in range(BOARD_RANGE):
            if self.board[0][0] != self.board[i][i]:
                break
            if i == (BOARD_RANGE - 1) and self.board[0][0] is not EMPTY:
                return self.board[0][0]

        # check diagonal /
        for i in range(BOARD_RANGE):
            if self.board[BOARD_RANGE - 1][0] != self.board[BOARD_RANGE - 1 - i][i]:
                break
            if i == (BOARD_RANGE - 1) and self.board[2][0] is not EMPTY:
                return self.board[BOARD_RANGE - 1][0]

        return None

    def check_draw(self):
        if all(cell is not EMPTY for row in self.board for cell in row):
            return True
        return False

    def get_board_state(self):
        result = None
        winner = self.check_winner()
        if winner:
            result = CROSS if winner == CROSS else NOUGHT
        elif self.check_draw():
            result = EMPTY
        return result


    def make_move(self, i, j, value):
        self.board[i][j] = value

    def minimax(self, depth, maximizing_player, player):
        game_result = self.get_board_state()
        if (game_result == CROSS and player == CROSS) or (game_result == NOUGHT and player == NOUGHT):
            return 10
        if (game_result == CROSS and player == NOUGHT) or (game_result == NOUGHT and player == CROSS):
            return -10
        if game_result == EMPTY:
            return 0

        opponent = CROSS
        if player == CROSS:
            opponent = NOUGHT

        if maximizing_player:
            max_score = float('-inf')
            for i in range(BOARD_RANGE):
                for j in range(BOARD_RANGE):
                    if self.board[i][j] is EMPTY:
                        self.board[i][j] = player  # try move
                        score = self.minimax(depth + 1, False, player)
                        self.board[i][j] = EMPTY  # cancel move

                        max_score = max(max_score, score)
            return max_score

        else:
            min_score = float('inf')
            for i in range(BOARD_RANGE):
                for j in range(BOARD_RANGE):
                    if self.board[i][j] == EMPTY:
                        self.board[i][j] = opponent  # cancel move
                        score = self.minimax(depth + 1, True, player)
                        self.board[i][j] = EMPTY  # cancel move
                        min_score = min(min_score, score)
            return min_score

    def find_best_move(self, player):
        best_score = float('-inf')
        best_i, best_j = None, None
        for i in range(BOARD_RANGE):
            for j in range(BOARD_RANGE):
                if self.board[i][j] == EMPTY:
                    self.board[i][j] = player # try move
                    score = self.minimax(0, False, player)
                    self.board[i][j] = EMPTY # cancel move
                    if score > best_score:
                        best_score = score
                        best_i = i
                        best_j = j
        return best_i, best_j

    def get_next_move(self, player):
        best_i, best_j = self.find_best_move(player)
        self.make_move(best_i, best_j, player)
