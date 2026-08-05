let sessionId = null;

const screenEl = document.getElementById("screen");
const scoreEl = document.getElementById("score");
const sqlInput = document.getElementById("sql-input");
const guessInput = document.getElementById("guess-input");

async function startGame() {
  const res = await fetch("/game/start", { method: "POST" });
  const data = await res.json();
  sessionId = data.session_id;
  scoreEl.textContent = data.score;
  screenEl.textContent = "novo pokémon capturado no radar.\nfaça sua primeira pergunta em SQL.";
  guessInput.value = "";
  sqlInput.value = "";
}

function formatRows(columns, rows) {
  if (!rows || rows.length === 0) return "(nenhuma linha retornada)";
  const header = columns.join(" | ");
  const lines = rows.map((r) => r.join(" | "));
  return [header, "-".repeat(header.length), ...lines].join("\n");
}

async function runQuery() {
  if (!sessionId) return;
  const sql = sqlInput.value.trim();
  if (!sql) return;

  screenEl.textContent = "consultando...";
  const res = await fetch("/game/query", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, sql }),
  });
  const data = await res.json();

  if (data.error) {
    screenEl.textContent = "erro: " + data.error;
  } else {
    screenEl.textContent = formatRows(data.columns, data.rows);
  }
  if (data.score !== undefined) scoreEl.textContent = data.score;
  handleGameOver(data);
}

async function makeGuess() {
  if (!sessionId) return;
  const name = guessInput.value.trim();
  if (!name) return;

  const res = await fetch("/game/guess", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, name }),
  });
  const data = await res.json();

  screenEl.textContent = data.message || data.error || "";
  if (data.score !== undefined) scoreEl.textContent = data.score;
  handleGameOver(data);
}

function handleGameOver(data) {
  if (data.sudden_death && !data.game_over) {
    screenEl.textContent += "\n\naviso: última chance! seu próximo palpite decide o jogo.";
  }
  if (data.game_over) {
    screenEl.textContent += "\n\nfim de jogo. clique em 'jogar de novo'.";
  }
}

document.getElementById("run-btn").addEventListener("click", runQuery);
document.getElementById("guess-btn").addEventListener("click", makeGuess);
document.getElementById("new-game-btn").addEventListener("click", startGame);

startGame();
