from flask import Flask, render_template, request, jsonify
from random import randint

app = Flask(__name__)

# Initialize the game board
board = [[0]*4 for _ in range(4)]

# Function to add a new tile to the board
def add_tile():
    empty_cells = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
    if empty_cells:
        i, j = empty_cells[randint(0, len(empty_cells) - 1)]
        board[i][j] = 2 if randint(0, 9) < 9 else 4

# Function to compress the board
def compress(board):
    new_board = [[0]*4 for _ in range(4)]
    for i in range(4):
        pos = 0
        for j in range(4):
            if board[i][j] != 0:
                new_board[i][pos] = board[i][j]
                pos += 1
    return new_board

# Function to merge tiles
def merge(board):
    for i in range(4):
        for j in range(3):
            if board[i][j] == board[i][j + 1] and board[i][j] != 0:
                board[i][j] *= 2
                board[i][j + 1] = 0
    return board

# Function to reverse the board
def reverse(board):
    new_board = []
    for i in range(4):
        new_board.append([])
        for j in range(4):
            new_board[i].append(board[i][3 - j])
    return new_board

# Function to transpose the board
def transpose(board):
    new_board = []
    for i in range(4):
        new_board.append([])
        for j in range(4):
            new_board[i].append(board[j][i])
    return new_board

# Function to check if the game is over
def game_over(board):
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                return False
    for i in range(3):
        for j in range(3):
            if board[i][j] == board[i + 1][j] or board[i][j] == board[i][j + 1]:
                return False
    return True

# Route for the game page
@app.route('/')
def index():
    return render_template('index.html', board=board)

# Route for handling moves
@app.route('/move', methods=['POST'])
def move():
    direction = request.json['direction']
    global board
    if direction == 'up':
        board = transpose(board)
        board = compress(board)
        board = merge(board)
        board = compress(board)
        board = transpose(board)
    elif direction == 'down':
        board = transpose(board)
        board = reverse(board)
        board = compress(board)
        board = merge(board)
        board = compress(board)
        board = reverse(board)
        board = transpose(board)
    elif direction == 'left':
        board = compress(board)
        board = merge(board)
        board = compress(board)
    elif direction == 'right':
        board = reverse(board)
        board = compress(board)
        board = merge(board)
        board = compress(board)
        board = reverse(board)
    add_tile()
    if game_over(board):
        return jsonify({'game_over': True})
    return jsonify({'board': board})

# Route for game over page
@app.route('/game-over')
def game_over_page():
    return render_template('game_over.html')

if __name__ == '__main__':
    app.run(debug=True)