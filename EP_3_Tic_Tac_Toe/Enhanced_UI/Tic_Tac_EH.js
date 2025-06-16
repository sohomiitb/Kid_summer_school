// Select all necessary DOM elements
const cells = document.querySelectorAll(".cell");
const statusText = document.getElementById("status");
const resetBtn = document.getElementById("reset");

// Initialize game state
let currentPlayer = "🐱";
let board = ["", "", "", "", "", "", "", "", ""];
let gameActive = true;

// Define all possible win conditions
const winConditions = [
  [0, 1, 2],
  [3, 4, 5],
  [6, 7, 8],
  [0, 3, 6],
  [1, 4, 7],
  [2, 5, 8],
  [0, 4, 8],
  [2, 4, 6],
];

// Check if the current player has won
function checkWin() {
  for (let i = 0; i < winConditions.length; i++) {
    const [a, b, c] = winConditions[i];
    if (board[a] && board[a] === board[b] && board[a] === board[c]) {
      statusText.textContent = `${currentPlayer} wins! 🎉`;
      gameActive = false;
      return;
    }
  }

  // Check for draw
  if (!board.includes("")) {
    statusText.textContent = "It's a draw! 🤝";
    gameActive = false;
  }
}

// Handle when a cell is clicked
function handleCellClick(event) {
  const index = event.target.dataset.index;

  // If the cell is already filled or game is over, ignore the click
  if (board[index] !== "" || !gameActive) return;

  // Update board state and cell content
  board[index] = currentPlayer;
  event.target.textContent = currentPlayer;

  // Check for a win or draw
  checkWin();

  // Switch player if the game is still active
  if (gameActive) {
    currentPlayer = currentPlayer === "🐱" ? "🐶" : "🐱";
    statusText.textContent = `Your turn: ${currentPlayer}`;
  }
}

// Reset the game to the initial state
function resetGame() {
  board = ["", "", "", "", "", "", "", "", ""];
  currentPlayer = "🐱";
  gameActive = true;
  statusText.textContent = `Your turn: ${currentPlayer}`;
  cells.forEach(cell => cell.textContent = "");
}

// Add event listeners
cells.forEach(cell => cell.addEventListener("click", handleCellClick));
resetBtn.addEventListener("click", resetGame);

// Set initial status
statusText.textContent = `Your turn: ${currentPlayer}`;
