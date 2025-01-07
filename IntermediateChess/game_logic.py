class ChessGame:
    def __init__(self):
        self.board = self.initialize_board()
        self.move_history = []
        self.redo_stack = []
        self.turn = "w"  # Initialize turn

    def initialize_board(self):
        # Initialize 8x8 chess board with starting positions
        board = [[None]*8 for _ in range(8)]

        # Place pawns
        for i in range(8):
            board[1][i] = "p"
            board[6][i] = "P"

        # Place pieces
        pieces = ["r", "n", "b", "q", "k", "b", "n", "r"]
        for i, piece in enumerate(pieces):
            board[0][i] = piece
            board[7][i] = piece.upper()

        return board

    def move_piece(self, start, end):
        # Validate move coordinates
        if not (0 <= start[0] < 8 and 0 <= start[1] < 8 and
                0 <= end[0] < 8 and 0 <= end[1] < 8):
            raise ValueError("Invalid move coordinates")

        # Check turn
        piece = self.board[start[0]][start[1]]
        if piece and piece.isupper() != (self.get_turn() == "w"):
            raise ValueError("Invalid turn")

        # Move piece
        self.board[end[0]][end[1]] = self.board[start[0]][start[1]]
        self.board[start[0]][start[1]] = None

        # Update move history and turn
        self.move_history.append((start, end))
        self.redo_stack.clear()
        self.set_turn("b" if self.get_turn() == "w" else "w")

    def undo_move(self):
        # Check move history
        if not self.move_history:
            raise ValueError("No moves to undo")

        # Undo last move
        start, end = self.move_history.pop()
        self.board[start[0]][start[1]] = self.board[end[0]][end[1]]
        self.board[end[0]][end[1]] = None

        # Update redo stack and turn
        self.redo_stack.append((start, end))
        self.set_turn("b" if self.get_turn() == "w" else "w")

    def redo_move(self):
        # Check redo stack
        if not self.redo_stack:
            raise ValueError("No moves to redo")

        # Redo last undone move
        start, end = self.redo_stack.pop()
        self.board[end[0]][end[1]] = self.board[start[0]][start[1]]
        self.board[start[0]][start[1]] = None

        # Update move history and turn
        self.move_history.append((start, end))
        self.set_turn("b" if self.get_turn() == "w" else "w")

    def get_board(self):
        return self.board

    def get_turn(self):
        return self.turn

    def set_turn(self, turn):
        self.turn = turn

    def get_valid_moves(self, start):
        # Get valid moves for a piece
        piece = self.board[start[0]][start[1]]
        if piece.isupper():
            # White pieces
            if piece == 'P':
                # Pawn
                valid_moves = self.get_pawn_moves(start)
            elif piece == 'N':
                # Knight
                valid_moves = self.get_knight_moves(start)
            elif piece == 'B':
                # Bishop
                valid_moves = self.get_bishop_moves(start)
            elif piece == 'R':
                # Rook
                valid_moves = self.get_rook_moves(start)
            elif piece == 'Q':
                # Queen
                valid_moves = self.get_queen_moves(start)
            elif piece == 'K':
                # King
                valid_moves = self.get_king_moves(start)
        else:
            # Black pieces
            if piece == 'p':
                # Pawn
                valid_moves = self.get_pawn_moves(start)
            elif piece == 'n':
                # Knight
                valid_moves = self.get_knight_moves(start)
            elif piece == 'b':
                # Bishop
                valid_moves = self.get_bishop_moves(start)
            elif piece == 'r':
                # Rook
                valid_moves = self.get_rook_moves(start)
            elif piece == 'q':
                # Queen
                valid_moves = self.get_queen_moves(start)
            elif piece == 'k':
                # King
                valid_moves = self.get_king_moves(start)

        return valid_moves

    def get_pawn_moves(self, start):
        # Get valid moves for a pawn
        valid_moves = []
        def get_pawn_moves(self, start):
        # Get valid moves for a pawn
        valid_moves = []
        if self.board[start[0]][start[1]].isupper():
            # White pawn
            if start[0] == 1:
                # Pawn can move two spaces on first move
                valid_moves.append([start[0] + 2, start[1]])
            valid_moves.append([start[0] + 1, start[1]])
        else:
            # Black pawn
            if start[0] == 6:
                # Pawn can move two spaces on first move
                valid_moves.append([start[0] - 2, start[1]])
            valid_moves.append([start[0] - 1, start[1]])

        return valid_moves

    def get_knight_moves(self, start):
        # Get valid moves for a knight
        valid_moves = []
        for i in [-2, -1, 1, 2]:
            for j in [-2, -1, 1, 2]:
                if abs(i) + abs(j) == 3:
                    valid_moves.append([start[0] + i, start[1] + j])

        return valid_moves

    def get_bishop_moves(self, start):
        # Get valid moves for a bishop
        valid_moves = []
        for i in [-1, 1]:
            for j in [-1, 1]:
                for k in range(1, 8):
                    if start[0] + i * k >= 0 and start[0] + i * k < 8 and start[1] + j * k >= 0 and start[1] + j * k < 8:
                        valid_moves.append([start[0] + i * k, start[1] + j * k])

        return valid_moves

    def get_rook_moves(self, start):
        # Get valid moves for a rook
        valid_moves = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 or j == 0:
                    for k in range(1, 8):
                        if start[0] + i * k >= 0 and start[0] + i * k < 8 and start[1] + j * k >= 0 and start[1] + j * k < 8:
                            valid_moves.append([start[0] + i * k, start[1] + j * k])

        return valid_moves

    def get_queen_moves(self, start):
        # Get valid moves for a queen
        valid_moves = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 or j == 0:
                    for k in range(1, 8):
                        if start[0] + i * k >= 0 and start[0] + i * k < 8 and start[1] + j * k >= 0 and start[1] + j * k < 8:
                            valid_moves.append([start[0] + i * k, start[1] + j * k])
                else:
                    for k in range(1, 8):
                        if start[0] + i * k >= 0 and start[0] + i * k < 8 and start[1] + j * k >= 0 and start[1] + j * k < 8:
                            valid_moves.append([start[0] + i * k, start[1] + j * k])

        return valid_moves

    def get_king_moves(self, start):
        # Get valid moves for a king
        valid_moves = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                end = [start[0] + i, start[1] + j]
                if end[0] >= 0 and end[0] < 8 and end[1] >= 0 and end[1] < 8:
                    valid_moves.append(end)

        return valid_moves

