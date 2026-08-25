import {formatTime, getElapsed} from './timer.js';

const STORAGE_KEY = 'sudoku-scores';

function readScores() {
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'); }
  catch (error) { return []; }
}

export function saveScore(difficulty, hintsUsed, showMessage) {
  const trimmedName = (window.prompt('Enter your name for the Top 10:', 'Player') || '').trim();
  if (!trimmedName) { showMessage('A name is required to save your score.', 'error'); return; }
  const scores = readScores();
  scores.push({name: trimmedName.slice(0, 20), time: getElapsed(), difficulty, hints: hintsUsed});
  scores.sort((a, b) => a.time - b.time);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(scores.slice(0, 10)));
  renderScores();
}

export function renderScores() {
  const scores = readScores();
  document.getElementById('scores-list').innerHTML = scores.map((score, index) => `<li><span class="rank">${String(index + 1).padStart(2, '0')}</span><strong>${escapeHtml(score.name)}</strong><span>${formatTime(score.time)} <small>${score.difficulty} · ${score.hints || 0} hints</small></span></li>`).join('');
  document.getElementById('empty-scores').hidden = scores.length > 0;
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}
