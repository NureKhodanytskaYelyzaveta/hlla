const express = require("express");
const cors = require("cors");
const fs = require("fs");

const app = express();
app.use(cors());
app.use(express.json());

let secretNumber = Math.floor(Math.random() * 100) + 1;
let attempts = 0;

let leaderboard = [];
let tournamentPlayers = [];
let tournamentResults = [];

let history = [];
if (fs.existsSync("history.json")) {
  history = JSON.parse(fs.readFileSync("history.json"));
}

app.get("/start", (req, res) => {
  secretNumber = Math.floor(Math.random() * 100) + 1;
  attempts = 0;
  res.json({ message: "Нова гру почато!" });
});

app.post("/guess", (req, res) => {
  const { number, player } = req.body;
  attempts++;

  if (number < secretNumber) {
    return res.json({ result: "Більше", attempts });
  }

  if (number > secretNumber) {
    return res.json({ result: "Менше", attempts });
  }

  const winRecord = {
    player,
    attempts,
    date: new Date().toLocaleString(),
  };

  leaderboard.push({ player, attempts });
  leaderboard.sort((a, b) => a.attempts - b.attempts);

  tournamentResults.push({ player, attempts });
  tournamentResults.sort((a, b) => a.attempts - b.attempts);

  history.push(winRecord);
  fs.writeFileSync("history.json", JSON.stringify(history, null, 2));

  res.json({ result: "Вгадав!", attempts });
});

app.get("/leaderboard", (req, res) => {
  res.json(leaderboard);
});

app.get("/history", (req, res) => {
  res.json(history);
});

app.post("/tournament/add", (req, res) => {
  const { player } = req.body;

  if (!tournamentPlayers.includes(player)) {
    tournamentPlayers.push(player);
  }

  res.json(tournamentPlayers);
});

app.get("/tournament/players", (req, res) => {
  res.json(tournamentPlayers);
});

app.get("/tournament/results", (req, res) => {
  res.json(tournamentResults);
});

app.post("/tournament/clear", (req, res) => {
  tournamentPlayers = [];
  tournamentResults = [];
  res.json({ message: "Турнір очищено" });
});

app.listen(5000, () => {
  console.log("Сервер запущено на порту 5000");
});