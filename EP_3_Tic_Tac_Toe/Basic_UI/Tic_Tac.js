const cells = document.querySelectorAll(".cell");
const statusText = document.getElementById("status");
const resetBtn = document.getElementById("reset");

let currentPlayer = "X";
let board = ["", "", "", "", "", "", "", "", ""];
let gameActive = true;

const winConditions = [
  [0,1,2],
  [3,4,5],
  [6,7,8],
  [0,3,6],
  [1,4,7],
  [2,5,8],
  [0,4,8],
  [2,4,6],
];

function checkWin() {
  for (const condition of winConditions) {
    const [a,b,c] = condition;
    if (board[a] && board[a] === board[b] && board[a] === board[c]) {
      statusText.textContent = `Player ${currentPlayer} Wins!`;
      gameActive = false;
      return;
    }
  }

  if (!board.includes("")) {
    statusText.textContent = "It's a Draw!";
    gameActive = false;
  }
}

function handleCellClick(e) {
  const index = e.target.dataset.index;
  if (board[index] || !gameActive) return;

  board[index] = currentPlayer;
  e.target.textContent = currentPlayer;

  checkWin();
  if (gameActive) {
    currentPlayer = currentPlayer === "X" ? "O" : "X";
    statusText.textContent = `Player ${currentPlayer}'s turn`;
  }
}

function resetGame() {
  board = ["", "", "", "", "", "", "", "", ""];
  currentPlayer = "X";
  gameActive = true;
  statusText.textContent = `Player ${currentPlayer}'s turn`;
  cells.forEach(cell => cell.textContent = "");
}

cells.forEach(cell => cell.addEventListener("click", handleCellClick));
resetBtn.addEventListener("click", resetGame);

statusText.textContent = `Player ${currentPlayer}'s turn`;
