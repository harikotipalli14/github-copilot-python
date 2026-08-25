"""Validation helpers and application-level input errors."""

from collections.abc import Iterable


class InvalidBoardError(ValueError):
    """Raised when a request does not contain a valid Sudoku board shape."""


class InvalidDifficultyError(ValueError):
    """Raised when a request uses an unsupported difficulty."""


class InvalidRequestError(ValueError):
    """Raised when a request payload is missing or malformed."""


def validate_difficulty(difficulty: str, supported: Iterable[str]) -> str:
    """Return a normalized difficulty or raise a meaningful client error."""
    normalized = (difficulty or "").lower()
    if normalized not in supported:
        raise InvalidDifficultyError("Difficulty must be easy, medium, or hard.")
    return normalized


def validate_board(board: object, size: int, empty: int = 0) -> list[list[int]]:
    """Validate a nine-by-nine integer grid without solving or revealing it."""
    if not isinstance(board, list) or len(board) != size:
        raise InvalidBoardError("Board must be a 9 by 9 grid of numbers.")
    if any(not isinstance(row, list) or len(row) != size for row in board):
        raise InvalidBoardError("Board must be a 9 by 9 grid of numbers.")
    if any(not isinstance(value, int) or value not in range(empty, size + 1)
           for row in board for value in row):
        raise InvalidBoardError("Board must contain numbers from 0 through 9.")
    return [row[:] for row in board]
