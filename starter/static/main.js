const SIZE = 9;
let puzzle = [];
let difficulty = 'medium';
let elapsed = 0;
let hintsUsed = 0;
let timerId;

const $ = (id) => document.getElementById(id);
const cells = () => [...document.querySelectorAll('.sudoku-cell')];
const formatTime = (seconds) => `${String(Math.floor(seconds / 60)).padStart(2, '0')}:${String(seconds % 60).padStart(2, '0')}`;
const boardValues = () => Array.from({length: SIZE}, (_, row) => Array.from({length: SIZE}, (_, col) => Number(document.querySelector(`[data-row="${row}"][data-col="${col}"]`).value) || 0));

function showMessage(text, tone = '') { $('message').textContent = text; $('message').className = `message ${tone}`; }
function startTimer() { clearInterval(timerId); timerId = setInterval(() => { elapsed += 1; $('timer').textContent = formatTime(elapsed); }, 1000); }
async function requestJson(url, options) {
  try {
    const response = await fetch(url, options);
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'The request could not be completed.');
    return data;
  } catch (error) {
    showMessage(error.message || 'The server is unavailable. Please try again.', 'error');
    return null;
  }
}

function renderPuzzle(nextPuzzle) {
  puzzle = nextPuzzle;
  const fragment = puzzle.flatMap((row, rowIndex) => row.map((value, colIndex) => {
    const input = document.createElement('input');
    input.className = `sudoku-cell box-${Math.floor(rowIndex / 3) * 3 + Math.floor(colIndex / 3)}`;
    input.type = 'text'; input.inputMode = 'numeric'; input.maxLength = 1;
    input.dataset.row = rowIndex; input.dataset.col = colIndex; input.setAttribute('role', 'gridcell');
    input.setAttribute('aria-label', `Row ${rowIndex + 1}, column ${colIndex + 1}`);
    if (value) { input.value = value; input.disabled = true; input.classList.add('prefilled'); }
    return input;
  })).reduce((boardFragment, input) => { boardFragment.appendChild(input); return boardFragment; }, document.createDocumentFragment());
  $('sudoku-board').replaceChildren(fragment);
}

function hasConflict(target) {
  const value = target.value;
  if (!value) return false;
  return cells().some((cell) => cell !== target && cell.value === value &&
    (cell.dataset.row === target.dataset.row || cell.dataset.col === target.dataset.col ||
      (Math.floor(cell.dataset.row / 3) === Math.floor(target.dataset.row / 3) && Math.floor(cell.dataset.col / 3) === Math.floor(target.dataset.col / 3))));
}

function updateInput(event) {
  const input = event.target;
  input.value = input.value.replace(/[^1-9]/g, '').slice(-1);
  input.classList.toggle('conflict', hasConflict(input));
  if (input.classList.contains('conflict')) showMessage('That number conflicts with this row, column, or square.', 'error');
  else if (!document.querySelector('.conflict')) showMessage('');
}

async function newGame() {
  difficulty = $('difficulty').value;
  const data = await requestJson(`/new?difficulty=${difficulty}`);
  if (!data) return;
  renderPuzzle(data.puzzle); elapsed = 0; $('timer').textContent = formatTime(elapsed); showMessage(''); startTimer();
  hintsUsed = 0;
}

function markIncorrect(incorrect) {
  const incorrectCells = new Set(incorrect.map(([row, col]) => `${row}-${col}`));
  cells().forEach((cell) => cell.classList.toggle('incorrect', incorrectCells.has(`${cell.dataset.row}-${cell.dataset.col}`)));
  return incorrectCells.size;
}

async function checkPuzzle() {
  const data = await requestJson('/check-puzzle', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({board: boardValues()})});
  if (!data) return;
  const incorrectCount = markIncorrect(data.incorrect);
  showMessage(incorrectCount ? 'Some entries need another look.' : 'No incorrect entries so far.', incorrectCount ? 'error' : 'success');
}

async function checkSolution() {
  const data = await requestJson('/check-solution', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({board: boardValues()})});
  if (!data) return;
  if (data.complete) { clearInterval(timerId); showMessage(`Solved in ${formatTime(elapsed)}. Excellent work.`, 'success'); saveScore(); }
  else showMessage('The puzzle is not complete yet.', 'error');
}

async function giveHint() {
  const data = await requestJson('/hint', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({board: boardValues()})});
  if (!data) return;
  const input = document.querySelector(`[data-row="${data.row}"][data-col="${data.col}"]`);
  input.value = data.value; input.disabled = true; input.classList.add('hinted'); hintsUsed += 1; showMessage('A correct cell has been locked in.', 'success');
}

function saveScore() {
  const name = window.prompt('Enter your name for the Top 10:', 'Player');
  const trimmedName = (name || '').trim();
  if (!trimmedName) { showMessage('A name is required to save your score.', 'error'); return; }
  const scores = JSON.parse(localStorage.getItem('sudoku-scores') || '[]');
  scores.push({name: trimmedName.slice(0, 20), time: elapsed, difficulty, hints: hintsUsed});
  scores.sort((a, b) => a.time - b.time); localStorage.setItem('sudoku-scores', JSON.stringify(scores.slice(0, 10))); renderScores();
}
function renderScores() {
  const scores = JSON.parse(localStorage.getItem('sudoku-scores') || '[]'); $('scores-list').innerHTML = scores.map((score, index) => `<li><span class="rank">${String(index + 1).padStart(2, '0')}</span><strong>${escapeHtml(score.name)}</strong><span>${formatTime(score.time)} <small>${score.difficulty} · ${score.hints || 0} hints</small></span></li>`).join(''); $('empty-scores').hidden = scores.length > 0;
}
function escapeHtml(text) { const div = document.createElement('div'); div.textContent = text; return div.innerHTML; }

$('sudoku-board').addEventListener('input', updateInput); $('new-game').addEventListener('click', newGame); $('check-puzzle').addEventListener('click', checkPuzzle); $('check-solution').addEventListener('click', checkSolution); $('hint').addEventListener('click', giveHint); $('theme-toggle').addEventListener('click', () => { document.body.classList.toggle('dark'); localStorage.setItem('sudoku-theme', document.body.classList.contains('dark') ? 'dark' : 'light'); });
if (localStorage.getItem('sudoku-theme') === 'dark') document.body.classList.add('dark');
renderScores(); newGame();