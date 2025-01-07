from flask import Flask, request, jsonify
from puzzle_generator import PuzzleGenerator

app = Flask(__name__)
puzzle_generator = PuzzleGenerator()
puzzles = {}

@app.route('/puzzles', methods=['POST'])
def create_puzzle():
    difficulty = request.json['difficulty']
    puzzle = puzzle_generator.generate_puzzle(difficulty)
    puzzle_id = len(puzzles)
    puzzles[puzzle_id] = {'puzzle': puzzle, 'ratings': []}
    return jsonify({'puzzle_id': puzzle_id})

@app.route('/puzzles/<int:puzzle_id>', methods=['GET'])
def get_puzzle(puzzle_id):
    if puzzle_id in puzzles:
        return jsonify({'puzzle': puzzles[puzzle_id]['puzzle']})
    return jsonify({'error': 'Puzzle not found'}), 404

@app.route('/puzzles/<int:puzzle_id>/rate', methods=['POST'])
def rate_puzzle(puzzle_id):
    rating = request.json['rating']
    if puzzle_id in puzzles:
        puzzles[puzzle_id]['ratings'].append(rating)
        return jsonify({'success': True})
    return jsonify({'error': 'Puzzle not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)