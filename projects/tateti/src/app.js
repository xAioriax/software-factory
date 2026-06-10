const STORAGE_KEY = 'software-factory-tateti-score-v2';
const WIN_LINES = [
  [0, 1, 2],
  [3, 4, 5],
  [6, 7, 8],
  [0, 3, 6],
  [1, 4, 7],
  [2, 5, 8],
  [0, 4, 8],
  [2, 4, 6]
];

const boardEl = document.querySelector('#board');
const statusEl = document.querySelector('#status');
const modeEl = document.querySelector('#mode');
const playerMarkEl = document.querySelector('#playerMark');
const restartButton = document.querySelector('#restart');
const resetScoreButton = document.querySelector('#resetScore');
const winsEl = document.querySelector('#wins');
const lossesEl = document.querySelector('#losses');
const drawsEl = document.querySelector('#draws');

let board = Array(9).fill(null);
let currentPlayer = 'X';
let gameActive = true;
let mode = 'local';
let humanMark = 'X';
let score = loadScore();

function loadScore() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
    return {
      wins: Number.isFinite(saved.wins) ? saved.wins : 0,
      losses: Number.isFinite(saved.losses) ? saved.losses : 0,
      draws: Number.isFinite(saved.draws) ? saved.draws : 0
    };
  } catch {
    return { wins: 0, losses: 0, draws: 0 };
  }
}

function saveScore() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(score));
}

function renderScore() {
  winsEl.textContent = score.wins;
  lossesEl.textContent = score.losses;
  drawsEl.textContent = score.draws;
}

function setStatus(message, type = '') {
  statusEl.textContent = message;
  statusEl.className = type ? `status ${type}` : 'status';
}

function renderBoard() {
  boardEl.innerHTML = '';

  board.forEach((mark, index) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'cell';
    button.textContent = mark || '';
    button.disabled = !gameActive || Boolean(mark) || (mode === 'cpu' && currentPlayer === cpuMark());
    button.setAttribute('aria-label', mark ? `Casilla ${index + 1}, ocupada por ${mark}` : `Casilla ${index + 1}, vacía`);

    if (mark) {
      button.classList.add(mark.toLowerCase());
    }

    button.addEventListener('click', () => play(index));
    boardEl.appendChild(button);
  });
}

function findWinningLine(player) {
  return WIN_LINES.find(([a, b, c]) => board[a] === player && board[b] === player && board[c] === player);
}

function isDraw() {
  return board.every(Boolean);
}

function finishGame(type) {
  gameActive = false;
  renderBoard();

  if (type === 'win') {
    score.wins += 1;
    setStatus(`¡Ganaste! ${currentPlayer === humanMark ? 'Nueva victoria.' : 'La computadora ganó.'}`, 'win');
  } else if (type === 'loss') {
    score.losses += 1;
    setStatus('Perdiste esta partida. Probá de nuevo.', 'loss');
  } else {
    score.draws += 1;
    setStatus('Empate. Nadie ganó esta vez.', 'draw');
  }

  saveScore();
  renderScore();
}

function switchTurn() {
  currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
  setStatus(`Turno de ${currentPlayer}`);
}

function play(index) {
  if (!gameActive || board[index] || (mode === 'cpu' && currentPlayer === cpuMark())) {
    return;
  }

  board[index] = currentPlayer;

  const winningLine = findWinningLine(currentPlayer);
  if (winningLine) {
    highlightWinningLine(winningLine);
    finishGame(currentPlayer === humanMark ? 'win' : 'loss');
    return;
  }

  if (isDraw()) {
    finishGame('draw');
    return;
  }

  switchTurn();

  if (mode === 'cpu' && currentPlayer === cpuMark()) {
    window.setTimeout(computerMove, 260);
  }
}

function cpuMark() {
  return humanMark === 'X' ? 'O' : 'X';
}

function highlightWinningLine(line) {
  [...boardEl.children].forEach((cell, index) => {
    if (line.includes(index)) {
      cell.classList.add('winning');
    }
  });
}

function computerMove() {
  if (!gameActive || currentPlayer !== cpuMark()) {
    return;
  }

  const cpu = cpuMark();
  const human = humanMark;
  const emptyIndexes = board
    .map((mark, index) => mark ? null : index)
    .filter((index) => index !== null);

  const winningMove = findMoveThatWins(cpu, emptyIndexes);
  const blockingMove = findMoveThatWins(human, emptyIndexes);
  const center = emptyIndexes.includes(4) ? 4 : null;
  const corner = emptyIndexes.find((index) => [0, 2, 6, 8].includes(index));
  const randomMove = emptyIndexes[Math.floor(Math.random() * emptyIndexes.length)];
  const chosen = winningMove ?? blockingMove ?? center ?? corner ?? randomMove;

  play(chosen);
}

function findMoveThatWins(player, indexes) {
  for (const index of indexes) {
    const copy = [...board];
    copy[index] = player;

    const wins = WIN_LINES.some(([a, b, c]) => copy[a] === player && copy[b] === player && copy[c] === player);
    if (wins) {
      return index;
    }
  }

  return null;
}

function restartGame() {
  board = Array(9).fill(null);
  currentPlayer = 'X';
  gameActive = true;
  setStatus('Turno de X');
  renderBoard();
}

function resetScore() {
  score = { wins: 0, losses: 0, draws: 0 };
  saveScore();
  renderScore();
  restartGame();
}

modeEl.addEventListener('change', () => {
  mode = modeEl.value;
  playerMarkEl.disabled = mode !== 'cpu';
  humanMark = mode === 'cpu' ? playerMarkEl.value : 'X';
  currentPlayer = 'X';
  gameActive = true;
  setStatus(mode === 'cpu' ? `Jugás con ${humanMark}. Empezá la partida.` : 'Turno de X');
  renderBoard();
});

playerMarkEl.addEventListener('change', () => {
  humanMark = playerMarkEl.value;
  currentPlayer = 'X';
  gameActive = true;
  setStatus(`Jugás con ${humanMark}. Empezá la partida.`);
  renderBoard();
});

restartButton.addEventListener('click', restartGame);
resetScoreButton.addEventListener('click', resetScore);

renderScore();
renderBoard();
