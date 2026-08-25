import sudoku_logic

from app import CURRENT, app


def test_invalid_difficulty_returns_consistent_error():
    response = app.test_client().get('/new?difficulty=expert')
    assert response.status_code == 400
    assert response.get_json() == {'error': 'Difficulty must be easy, medium, or hard.'}


def test_check_solution_requires_an_active_game():
    CURRENT.update(puzzle=None, solution=None)
    response = app.test_client().post('/check-solution', json={'board': sudoku_logic.create_empty_board()})
    assert response.status_code == 400
    assert response.get_json() == {'error': 'No game in progress.'}


def test_routes_reject_malformed_payloads():
    client = app.test_client()
    client.get('/new')
    response = client.post('/hint', json={'board': 'invalid'})
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Board must be a 9 by 9 grid of numbers.'


def test_legacy_check_preserves_combined_response():
    client = app.test_client()
    client.get('/new')
    response = client.post('/check', json={'board': sudoku_logic.create_empty_board()})
    assert response.status_code == 200
    assert set(response.get_json()) == {'incorrect', 'complete'}
