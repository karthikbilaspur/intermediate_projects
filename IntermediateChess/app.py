from flask import Flask, render_template, request, jsonify, send_file
from flask_caching import Cache
from game_logic import ChessGame

app = Flask(__name__)

cache = Cache(app, config={"CACHE_TYPE": "SimpleCache"})

game = ChessGame()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def move_piece():
    data = request.get_json()
    start = data["start"]
    end = data["end"]
    game.move_piece(start, end)
    return jsonify(game.get_board())

@app.route("/undo", methods=["POST"])
def undo_move():
    game.undo_move()
    return jsonify(game.get_board())

@app.route("/redo", methods=["POST"])
def redo_move():
    game.redo_move()
    return jsonify(game.get_board())

@app.route('/undo', methods=['POST'])
def undo_move():
    game.undo_move()
    return jsonify(game.get_board())

@app.route('/redo', methods=['POST'])
def redo_move():
    game.redo_move()
    return jsonify(game.get_board())

@app.route('/get-valid-moves', methods=['POST'])
def get_valid_moves():
    data = request.get_json()
    start = data['start']
    valid_moves = game.get_valid_moves(start)
    return jsonify(valid_moves)


@app.route("/piece/<piece>")
def get_piece_image(piece):
    return send_file(f"static/img/{piece}.png")

if __name__ == "__main__":
    app.run(debug=True)