let elapsed = 0;
let timerId;

export const formatTime = (seconds) => `${String(Math.floor(seconds / 60)).padStart(2, '0')}:${String(seconds % 60).padStart(2, '0')}`;
export const getElapsed = () => elapsed;

export function resetTimer() {
  elapsed = 0;
  document.getElementById('timer').textContent = formatTime(elapsed);
}

export function startTimer() {
  clearInterval(timerId);
  timerId = setInterval(() => {
    elapsed += 1;
    document.getElementById('timer').textContent = formatTime(elapsed);
  }, 1000);
}

export function stopTimer() { clearInterval(timerId); }
