Copilot Instructions

Project

Build and maintain a modular Flask Sudoku application.

Code Standards

- Use clean, readable Python following PEP 8.
- Keep logic modular and reusable.
- Separate Flask routes, Sudoku logic, and UI logic.
- Preserve existing functionality when adding features.
- Use clear variable and function names.
- Handle errors gracefully.
- Add or update tests for significant changes.

Sudoku Requirements

- Generate Easy, Medium, and Hard puzzles.
- Every generated puzzle must have exactly one solution.
- Prefilled and hinted cells must remain locked.
- Validate user input without revealing solutions.

Game Features

- Check Puzzle highlights incorrect entries only.
- Check Solution validates the complete puzzle only when clicked.
- Timer stops only after a correct Check Solution.
- Hints must be counted and reset for every new game.
- New Game must not clear the leaderboard.

Leaderboard

- Store scores in browser localStorage.
- Save player name, completion time, difficulty, and hints used.
- After a correct Check Solution, require the player to enter a non-empty name before saving the score.
- Keep only the Top 10 scores.
- Persist scores across page refreshes and new games.

UI

- Use responsive CSS for desktop, tablet, and mobile.
- Alternate background colors between 3×3 Sudoku boxes.
- Support light and dark modes.
- Keep text, buttons, and the leaderboard readable at all screen sizes.

Copilot Behavior

Before making major changes:

1. Explain the implementation approach.
2. Identify possible risks or edge cases.
3. Keep changes limited to the requested feature.
4. Do not add unrelated functionality.
5. Explain important changes after implementation.

Submission Response Requirements

When completing a significant change or refactor, provide a concise implementation summary that includes:

- Which files or modules were changed and the responsibility of each module.
- How large or legacy code was split into modular, reusable functions, classes, utilities, or services.
- Specific examples of error handling, including caught exceptions, API or validation errors, logging, and user-facing fallback messages where applicable.
- Where comments, docstrings, or documentation were added or updated and how they clarify non-obvious behavior.
- The exact commands used to run the application and tests, plus the observed result.
- Any known limitations, skipped checks, or remaining risks.

Do not claim that the application builds, runs, or passes tests unless you actually verified it. Use file paths and function or class names as supporting references. Keep the summary professional and specific rather than using generic praise.