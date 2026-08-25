"""Compatibility exports for the extracted puzzle service."""

from app.services.puzzle_service import (BOX_SIZE, DIFFICULTIES, EMPTY, SIZE,
                                          count_solutions, create_empty_board,
                                          deep_copy, fill_board, generate_puzzle,
                                          is_safe, is_valid_board, remove_cells)
