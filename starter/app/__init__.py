"""Flask application factory for the Sudoku game."""

from flask import Flask

from app.routes import sudoku_bp
from app.services.game_service import CURRENT


def create_app() -> Flask:
    """Create and configure the Flask application."""
    application = Flask(__name__, template_folder="../templates",
                        static_folder="../static")
    application.register_blueprint(sudoku_bp)
    return application


app = create_app()

__all__ = ["CURRENT", "app", "create_app"]
