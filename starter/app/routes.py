"""Thin HTTP routes for the Sudoku application."""

from flask import Blueprint, jsonify, render_template, request

from app.services import game_service
from app.utils.validators import (InvalidBoardError, InvalidDifficultyError,
                                  validate_board)

sudoku_bp = Blueprint("sudoku", __name__)


def _request_board():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        raise InvalidBoardError("Board must be a 9 by 9 grid of numbers.")
    return validate_board(payload.get("board"), 9)


def _error_response(error):
    return jsonify({"error": str(error)}), 400


@sudoku_bp.get("/")
def index():
    return render_template("index.html")


@sudoku_bp.get("/new")
def new_game():
    try:
        difficulty = request.args.get("difficulty", "medium")
        puzzle, difficulty = game_service.start_game(difficulty)
        return jsonify({"puzzle": puzzle, "difficulty": difficulty})
    except InvalidDifficultyError as error:
        return _error_response(error)


@sudoku_bp.post("/check-puzzle")
def check_puzzle():
    try:
        return jsonify({"incorrect": game_service.check_puzzle(_request_board())})
    except (InvalidBoardError, game_service.GameNotStartedError) as error:
        return _error_response(error)


@sudoku_bp.post("/check-solution")
def check_solution():
    try:
        return jsonify({"complete": game_service.check_solution(_request_board())})
    except (InvalidBoardError, game_service.GameNotStartedError) as error:
        return _error_response(error)


@sudoku_bp.post("/check")
def check_legacy():
    try:
        board = _request_board()
        incorrect = game_service.check_puzzle(board)
        complete = game_service.check_solution(board)
        return jsonify({"incorrect": incorrect, "complete": complete})
    except (InvalidBoardError, game_service.GameNotStartedError) as error:
        return _error_response(error)


@sudoku_bp.post("/hint")
def hint():
    try:
        return jsonify(game_service.provide_hint(_request_board()))
    except (InvalidBoardError, game_service.GameNotStartedError,
            game_service.NoHintAvailableError) as error:
        return _error_response(error)
