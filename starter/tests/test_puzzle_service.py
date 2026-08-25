import pytest

from app.services import puzzle_service
from app.utils.validators import InvalidDifficultyError, validate_difficulty


def test_each_difficulty_generates_a_unique_puzzle():
    for clues in puzzle_service.DIFFICULTIES.values():
        puzzle, solution = puzzle_service.generate_puzzle(clues)
        assert len(puzzle) == puzzle_service.SIZE
        assert all(len(row) == puzzle_service.SIZE for row in puzzle)
        assert puzzle_service.count_solutions(puzzle) == 1
        assert all(value in range(1, 10) for row in solution for value in row)


def test_invalid_difficulty_has_a_meaningful_error():
    with pytest.raises(InvalidDifficultyError, match="Difficulty must be easy"):
        validate_difficulty("expert", puzzle_service.DIFFICULTIES)


def test_invalid_board_shape_is_rejected():
    assert not puzzle_service.is_valid_board([[1, 2, 3]])
    assert not puzzle_service.is_valid_board("not a board")
