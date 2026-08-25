const SIZE = 9;

export const cells = () => [...document.querySelectorAll('.sudoku-cell')];
export const boardValues = () => Array.from({length: SIZE}, (_, row) => Array.from({length: SIZE}, (_, col) => Number(document.querySelector(`[data-row="${row}"][data-col="${col}"]`).value) || 0));

export function renderPuzzle(puzzle) {
  const fragment = puzzle.flatMap((row, rowIndex) => row.map((value, colIndex) => {
    const input = document.createElement('input');
    input.className = `sudoku-cell box-${Math.floor(rowIndex / 3) * 3 + Math.floor(colIndex / 3)}`;
    input.type = 'text'; input.inputMode = 'numeric'; input.maxLength = 1;
    input.dataset.row = rowIndex; input.dataset.col = colIndex; input.setAttribute('role', 'gridcell');
    input.setAttribute('aria-label', `Row ${rowIndex + 1}, column ${colIndex + 1}`);
    if (value) { input.value = value; input.disabled = true; input.classList.add('prefilled'); }
    return input;
  })).reduce((boardFragment, input) => { boardFragment.appendChild(input); return boardFragment; }, document.createDocumentFragment());
  document.getElementById('sudoku-board').replaceChildren(fragment);
}

function hasConflict(target) {
  const value = target.value;
  if (!value) return false;
  return cells().some((cell) => cell !== target && cell.value === value &&
    (cell.dataset.row === target.dataset.row || cell.dataset.col === target.dataset.col ||
      (Math.floor(cell.dataset.row / 3) === Math.floor(target.dataset.row / 3) && Math.floor(cell.dataset.col / 3) === Math.floor(target.dataset.col / 3))));
}

export function updateInput(event, showMessage) {
  const input = event.target;
  input.value = input.value.replace(/[^1-9]/g, '').slice(-1);
  input.classList.toggle('conflict', hasConflict(input));
  if (input.classList.contains('conflict')) showMessage('That number conflicts with this row, column, or square.', 'error');
  else if (!document.querySelector('.conflict')) showMessage('');
}

export function markIncorrect(incorrect) {
  const incorrectCells = new Set(incorrect.map(([row, col]) => `${row}-${col}`));
  cells().forEach((cell) => cell.classList.toggle('incorrect', incorrectCells.has(`${cell.dataset.row}-${cell.dataset.col}`)));
  return incorrectCells.size;
}
