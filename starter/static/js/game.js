import {requestJson} from './api.js';
import {boardValues, markIncorrect, renderPuzzle, updateInput} from './board.js';
import {formatTime, getElapsed, resetTimer, startTimer, stopTimer} from './timer.js';
import {saveScore} from './leaderboard.js';

export function bindGame(showMessage) {
  let difficulty = 'medium';
  let hintsUsed = 0;
  const board = document.getElementById('sudoku-board');

  async function newGame() {
    difficulty = document.getElementById('difficulty').value;
    const data = await requestJson(`/new?difficulty=${difficulty}`, undefined, showMessage);
    if (!data) return;
    renderPuzzle(data.puzzle); hintsUsed = 0; resetTimer(); showMessage(''); startTimer();
  }

  async function checkPuzzle() {
    const data = await requestJson('/check-puzzle', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({board: boardValues()})}, showMessage);
    if (!data) return;
    const incorrectCount = markIncorrect(data.incorrect);
    showMessage(incorrectCount ? 'Some entries need another look.' : 'No incorrect entries so far.', incorrectCount ? 'error' : 'success');
  }

  async function checkSolution() {
    const data = await requestJson('/check-solution', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({board: boardValues()})}, showMessage);
    if (!data) return;
    if (data.complete) { stopTimer(); showMessage(`Solved in ${formatTime(getElapsed())}. Excellent work.`, 'success'); saveScore(difficulty, hintsUsed, showMessage); }
    else showMessage('The puzzle is not complete yet.', 'error');
  }

  async function giveHint() {
    const data = await requestJson('/hint', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({board: boardValues()})}, showMessage);
    if (!data) return;
    const input = document.querySelector(`[data-row="${data.row}"][data-col="${data.col}"]`);
    input.value = data.value; input.disabled = true; input.classList.add('hinted'); hintsUsed += 1; showMessage('A correct cell has been locked in.', 'success');
  }

  board.addEventListener('input', (event) => updateInput(event, showMessage));
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('check-puzzle').addEventListener('click', checkPuzzle);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  document.getElementById('hint').addEventListener('click', giveHint);
  newGame();
}
