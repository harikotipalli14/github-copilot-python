from flask import Flask, jsonify, render_template, request
import sudoku_logic

app = Flask(__name__)

# Keep a simple in-memory store for current puzzle and solution
CURRENT: dict[str, list[list[int]] | None] = {'puzzle': None, 'solution': None}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new')
def new_game():
    difficulty = request.args.get('difficulty', 'medium').lower()
    if difficulty not in sudoku_logic.DIFFICULTIES:
        return jsonify({'error': 'Difficulty must be easy, medium, or hard.'}), 400
    puzzle, solution = sudoku_logic.generate_puzzle(sudoku_logic.DIFFICULTIES[difficulty])
    CURRENT.update(puzzle=puzzle, solution=solution)
    return jsonify({'puzzle': puzzle, 'difficulty': difficulty})


def _get_board():
    board = (request.get_json(silent=True) or {}).get('board')
    if not sudoku_logic.is_valid_board(board or []):
        return None
    return [list(row) for row in board]

def _incorrect_cells(board, solution):
    return [[row, col] for row in range(sudoku_logic.SIZE)
            for col in range(sudoku_logic.SIZE)
            if board[row][col] not in (sudoku_logic.EMPTY, solution[row][col])]


def _validated_board():
    board = _get_board()
    solution = CURRENT.get('solution')
    if solution is None:
        return None, jsonify({'error': 'No game in progress.'}), 400
    if board is None:
        return None, jsonify({'error': 'Board must be a 9 by 9 grid of numbers.'}), 400
    return (board, solution), None, None


@app.route('/check-puzzle', methods=['POST'])
def check_puzzle():
    validated, error, status = _validated_board()
    if error:
        return error, status
    board, solution = validated
    return jsonify({'incorrect': _incorrect_cells(board, solution)})


@app.route('/check-solution', methods=['POST'])
def check_solution():
    validated, error, status = _validated_board()
    if error:
        return error, status
    board, solution = validated
    incorrect = _incorrect_cells(board, solution)
    complete = not incorrect and all(value for row in board for value in row)
    return jsonify({'complete': complete})


@app.route('/check', methods=['POST'])
def check_legacy():
    validated, error, status = _validated_board()
    if error:
        return error, status
    board, solution = validated
    incorrect = _incorrect_cells(board, solution)
    complete = not incorrect and all(value for row in board for value in row)
    return jsonify({'incorrect': incorrect, 'complete': complete})


@app.route('/hint', methods=['POST'])
def hint():
    board = _get_board()
    solution = CURRENT.get('solution')
    if solution is None:
        return jsonify({'error': 'No game in progress.'}), 400
    if board is None:
        return jsonify({'error': 'Board must be a 9 by 9 grid of numbers.'}), 400
    for row in range(sudoku_logic.SIZE):
        for col in range(sudoku_logic.SIZE):
            if board[row][col] == sudoku_logic.EMPTY:
                return jsonify({'row': row, 'col': col, 'value': solution[row][col]})
    return jsonify({'error': 'No empty cells remain.'}), 400

if __name__ == '__main__':
    app.run(debug=True)