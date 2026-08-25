"""Sudoku generation and solving business logic."""

from __future__ import annotations

import copy
import random

SIZE = 9
BOX_SIZE = 3
EMPTY = 0
DIFFICULTIES = {"easy": 40, "medium": 32, "hard": 27}


def deep_copy(board: list[list[int]]) -> list[list[int]]:
    """Return an independent copy of a Sudoku board."""
    return copy.deepcopy(board)


def create_empty_board() -> list[list[int]]:
    """Create a blank Sudoku board."""
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]


def is_safe(board: list[list[int]], row: int, col: int, number: int) -> bool:
    """Check whether a number can be placed at a board position."""
    if any(board[row][column] == number for column in range(SIZE)):
        return False
    if any(board[index][col] == number for index in range(SIZE)):
        return False
    box_row, box_col = row - row % BOX_SIZE, col - col % BOX_SIZE
    return all(board[box_row + r][box_col + c] != number
               for r in range(BOX_SIZE) for c in range(BOX_SIZE))


def _find_empty(board: list[list[int]]) -> tuple[int, int] | None:
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                return row, col
    return None


def fill_board(board: list[list[int]]) -> bool:
    """Fill a board with backtracking and randomized candidate ordering."""
    location = _find_empty(board)
    if location is None:
        return True
    row, col = location
    candidates = list(range(1, SIZE + 1))
    random.shuffle(candidates)
    for number in candidates:
        if is_safe(board, row, col, number):
            board[row][col] = number
            if fill_board(board):
                return True
            board[row][col] = EMPTY
    return False


def count_solutions(board: list[list[int]], limit: int = 2) -> int:
    """Count solutions, stopping at ``limit`` to make uniqueness checks faster."""
    location = _find_empty(board)
    if location is None:
        return 1
    row, col = location
    total = 0
    for number in range(1, SIZE + 1):
        if is_safe(board, row, col, number):
            board[row][col] = number
            total += count_solutions(board, limit)
            board[row][col] = EMPTY
            if total >= limit:
                return total
    return total


def remove_cells(board: list[list[int]], clues: int) -> None:
    """Remove cells only when the remaining puzzle still has one solution."""
    clues = max(17, min(SIZE * SIZE, clues))
    cells = list(range(SIZE * SIZE))
    random.shuffle(cells)
    for cell in cells:
        if sum(value != EMPTY for row in board for value in row) <= clues:
            return
        row, col = divmod(cell, SIZE)
        original = board[row][col]
        board[row][col] = EMPTY
        if count_solutions(deep_copy(board)) != 1:
            board[row][col] = original


def generate_puzzle(clues: int = DIFFICULTIES["medium"]):
    """Generate a puzzle and its solution, preserving exactly one solution."""
    board = create_empty_board()
    fill_board(board)
    solution = deep_copy(board)
    remove_cells(board, clues)
    return board, solution


def is_valid_board(board: object) -> bool:
    """Return whether a value has the expected dimensions and cell range."""
    if not isinstance(board, list):
        return False
    return all(isinstance(row, list) for row in board) and len(board) == SIZE \
        and all(len(row) == SIZE for row in board) \
        and all(isinstance(value, int) and value in range(EMPTY, SIZE + 1)
                for row in board for value in row)
