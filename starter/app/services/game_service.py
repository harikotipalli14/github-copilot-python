"""Game state and player-facing Sudoku operations."""

from app.services import puzzle_service
from app.utils.validators import validate_board, validate_difficulty

CURRENT = {"puzzle": None, "solution": None}


class GameNotStartedError(ValueError):
    """Raised when an operation requires an active puzzle."""


class NoHintAvailableError(ValueError):
    """Raised when an active board has no empty cells."""


def start_game(difficulty: str):
    """Generate and store a new game, returning its public puzzle data."""
    difficulty = validate_difficulty(difficulty, puzzle_service.DIFFICULTIES)
    puzzle, solution = puzzle_service.generate_puzzle(
        puzzle_service.DIFFICULTIES[difficulty])
    CURRENT.update(puzzle=puzzle, solution=solution)
    return puzzle, difficulty


def _active_solution():
    solution = CURRENT.get("solution")
    if solution is None:
        raise GameNotStartedError("No game in progress.")
    return solution


def _incorrect_cells(board, solution):
    """Identify wrong filled cells while allowing unfinished cells."""
    return [[row, col] for row in range(puzzle_service.SIZE)
            for col in range(puzzle_service.SIZE)
            if board[row][col] not in (puzzle_service.EMPTY, solution[row][col])]


def check_puzzle(board):
    """Validate a partial board and return coordinates of incorrect entries."""
    board = validate_board(board, puzzle_service.SIZE)
    return _incorrect_cells(board, _active_solution())


def check_solution(board):
    """Return whether a submitted board completely matches the solution."""
    board = validate_board(board, puzzle_service.SIZE)
    solution = _active_solution()
    incorrect = _incorrect_cells(board, solution)
    return not incorrect and all(value for row in board for value in row)


def provide_hint(board):
    """Return and identify the first empty cell without exposing the full solution."""
    board = validate_board(board, puzzle_service.SIZE)
    solution = _active_solution()
    for row in range(puzzle_service.SIZE):
        for col in range(puzzle_service.SIZE):
            if board[row][col] == puzzle_service.EMPTY:
                return {"row": row, "col": col, "value": solution[row][col]}
    raise NoHintAvailableError("No empty cells remain.")
