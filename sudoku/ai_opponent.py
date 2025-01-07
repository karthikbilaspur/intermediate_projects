import random

class AIOpponent:
    def __init__(self, difficulty):
        self.difficulty = difficulty

    def generate_move(self, board):
        if self.difficulty == 'easy':
            # Random empty cell selection
            return random.choice([(i, j) for i in range(9) for j in range(9) if board[i][j] == 0])

        elif self.difficulty == 'medium':
            # Prioritize cells with fewer possible values
            possible_values = self.calculate_possible_values(board)
            min_values = min(len(values) for values in possible_values)
            cells = [(i, j) for i in range(9) for j in range(9) if len(possible_values[i][j]) == min_values]
            return random.choice(cells)

        elif self.difficulty == 'hard':
            # Use constraint satisfaction algorithm
            return self.constraint_satisfaction(board)

    def calculate_possible_values(self, board):
        # Calculate possible values for each cell
        possible_values = [[[] for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    for num in range(1, 10):
                        if self.is_valid_move(board, i, j, num):
                            possible_values[i][j].append(num)
        return possible_values

    def is_valid_move(self, board, row, col, num):
        # Check if move is valid
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
        sub_grid_row = row // 3 * 3
        sub_grid_col = col // 3 * 3
        for i in range(3):
            for j in range(3):
                if board[sub_grid_row + i][sub_grid_col + j] == num:
                    return False
        return True

    def constraint_satisfaction(self, board):
        # Constraint satisfaction algorithm using backtracking
        def is_valid(board, row, col, num):
            for i in range(9):
                if board[row][i] == num or board[i][col] == num:
                    return False
            sub_grid_row = row // 3 * 3
            sub_grid_col = col // 3 * 3
            for i in range(3):
                for j in range(3):
                    if board[sub_grid_row + i][sub_grid_col + j] == num:
                        return False
            return True

        def solve(board):
            for i in range(9):
                for j in range(9):
                    if board[i][j] == 0:
                        numbers = list(range(1, 10))
                        random.shuffle(numbers)  # Randomize number order
                        for num in numbers:
                            if is_valid(board, i, j, num):
                                board[i][j] = num
                                if solve(board):
                                    return True
                                board[i][j] = 0
                        return False
            return True

        # Create copy of board to avoid modifying original
        board_copy = [row[:] for row in board]
        solve(board_copy)
        # Find first empty cell in solved board
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)