class Sudoku:
    def __init__(self, board):
        self.board = board

    def is_valid(self, row, col, num):
        for i in range(9):
            if self.board[row][i] == num or self.board[i][col] == num:
                return False
        sub_grid_row = row // 3 * 3
        sub_grid_col = col // 3 * 3
        for i in range(3):
            for j in range(3):
                if self.board[sub_grid_row + i][sub_grid_col + j] == num:
                    return False
        return True

    def solve(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    for num in range(1, 10):
                        if self.is_valid(i, j, num):
                            self.board[i][j] = num
                            if self.solve():
                                return True
                            self.board[i][j] = 0
                    return False
        return True

    def print_board(self):
        for i in range(9):
            for j in range(9):
                print(self.board[i][j], end=' ')
                if (j + 1) % 3 == 0 and j < 8:
                    print('|', end=' ')
            print()
            if (i + 1) % 3 == 0 and i < 8:
                print('-' * 21)