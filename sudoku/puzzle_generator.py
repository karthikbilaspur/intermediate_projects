import random
from sudoku import Sudoku

class PuzzleGenerator:
    def __init__(self):
        self.sudoku = Sudoku([[0]*9 for _ in range(9)])

    def generate_puzzle(self, difficulty):
        self.sudoku.solve()
        difficulty_levels = {
            'easy': (30, 40),
            'medium': (45, 55),
            'hard': (60, 70),
            'expert': (75, 85)
        }
        remove_range = difficulty_levels[difficulty]
        remove_count = random.randint(*remove_range)
        removed_cells = []
        for _ in range(remove_count):
            while True:
                row = random.randint(0, 8)
                col = random.randint(0, 8)
                if (row, col) not in removed_cells:
                    removed_cells.append((row, col))
                    break
            self.sudoku.board[row][col] = 0
        return self.sudoku.board

    def is_valid_puzzle(self, board):
        sudoku = Sudoku(board)
        solutions = 0
        def solve(board):
            nonlocal solutions
            for i in range(9):
                for j in range(9):
                    if board[i][j] == 0:
                        for num in range(1, 10):
                            if sudoku.is_valid(i, j, num):
                                board[i][j] = num
                                solve(board)
                                board[i][j] = 0
                        return
            solutions += 1
        solve(board)
        return solutions == 1

    def share_puzzle(self, puzzle):
        puzzle_str = ''
        for row in puzzle:
            puzzle_str += ''.join(map(str, row)) + '\n'
        return puzzle_str

    def load_puzzle(self, puzzle_str):
        puzzle = []
        for row_str in puzzle_str.split('\n'):
            row = [int(num) for num in row_str]
            puzzle.append(row)
        return puzzle