import {bindGame} from './js/game.js';
import {renderScores} from './js/leaderboard.js';

function showMessage(text, tone = '') {
  const message = document.getElementById('message');
  message.textContent = text;
  message.className = `message ${tone}`;
}

document.getElementById('theme-toggle').addEventListener('click', () => {
  document.body.classList.toggle('dark');
  localStorage.setItem('sudoku-theme', document.body.classList.contains('dark') ? 'dark' : 'light');
});
if (localStorage.getItem('sudoku-theme') === 'dark') document.body.classList.add('dark');
renderScores();
bindGame(showMessage);
