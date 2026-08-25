import sudoku_logic
from app import CURRENT, app


def test_generated_board_has_nine_rows_and_columns():
    puzzle, solution = sudoku_logic.generate_puzzle(35)

    assert len(puzzle) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in puzzle)
    assert len(solution) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in solution)


def test_new_game_returns_a_puzzle():
    client = app.test_client()

    response = client.get('/new?clues=40')

    assert response.status_code == 200
    assert len(response.get_json()['puzzle']) == sudoku_logic.SIZE


def test_check_returns_incorrect_cells():
    client = app.test_client()
    client.get('/new')

    response = client.post('/check', json={'board': sudoku_logic.create_empty_board()})

    assert response.status_code == 200
    assert response.get_json()['incorrect'] == []
    assert response.get_json()['complete'] is False


def test_generated_puzzle_has_one_solution_for_each_difficulty():
    for clues in sudoku_logic.DIFFICULTIES.values():
        puzzle, _ = sudoku_logic.generate_puzzle(clues)
        assert sudoku_logic.count_solutions(puzzle) == 1


def test_hint_returns_a_solution_value():
    client = app.test_client()
    puzzle = client.get('/new?difficulty=easy').get_json()['puzzle']
    response = client.post('/hint', json={'board': puzzle})

    assert response.status_code == 200
    assert response.get_json()['value'] in range(1, 10)


def test_check_puzzle_returns_only_incorrect_cells():
    client = app.test_client()
    puzzle = client.get('/new').get_json()['puzzle']
    board = [row[:] for row in puzzle]
    empty = next((row, col) for row in range(9) for col in range(9)
                 if board[row][col] == sudoku_logic.EMPTY)
    row, col = empty
    board[row][col] = 1 if CURRENT['solution'][row][col] != 1 else 2

    response = client.post('/check-puzzle', json={'board': board})

    assert response.status_code == 200
    assert response.get_json()['incorrect'] == [[row, col]]


def test_check_solution_reports_completion_without_revealing_solution():
    client = app.test_client()
    client.get('/new')

    response = client.post('/check-solution', json={'board': CURRENT['solution']})

    assert response.status_code == 200
    assert response.get_json() == {'complete': True}


def test_check_puzzle_rejects_invalid_board():
    client = app.test_client()
    client.get('/new')

    response = client.post('/check-puzzle', json={'board': []})

    assert response.status_code == 400
    assert response.get_json()['error'] == 'Board must be a 9 by 9 grid of numbers.'