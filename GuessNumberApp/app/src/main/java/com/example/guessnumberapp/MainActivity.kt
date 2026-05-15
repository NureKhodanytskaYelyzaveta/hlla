package com.example.guessnumberapp

import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import kotlinx.coroutines.launch
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST

data class StartResponse(val message: String)
data class GuessRequest(val number: Int, val player: String)
data class GuessResponse(val result: String, val attempts: Int)
data class LeaderboardEntry(val player: String, val attempts: Int)
data class HistoryEntry(val player: String, val attempts: Int, val date: String)
data class TournamentRequest(val player: String)

interface GameApi {
    @GET("start") suspend fun startGame(): StartResponse
    @POST("guess") suspend fun checkGuess(@Body req: GuessRequest): GuessResponse
    @GET("leaderboard") suspend fun getLeaderboard(): List<LeaderboardEntry>
    @GET("history") suspend fun getHistory(): List<HistoryEntry>
    @GET("tournament/players") suspend fun getTournamentPlayers(): List<String>
    @GET("tournament/results") suspend fun getTournamentResults(): List<LeaderboardEntry>
    @POST("tournament/add") suspend fun addToTournament(@Body req: TournamentRequest): List<String>
    @POST("tournament/clear") suspend fun clearTournament(): Map<String, String>
}

class MainActivity : AppCompatActivity() {

    private lateinit var api: GameApi
    private var currentAttempts = 0
    private var isGameWon = false
    private var currentPlayer = ""

    private lateinit var etPlayer: android.widget.EditText
    private lateinit var etGuess: android.widget.EditText
    private lateinit var btnAddTournament: android.widget.Button
    private lateinit var btnClearTournament: android.widget.Button
    private lateinit var btnStartGame: android.widget.Button
    private lateinit var btnCheck: android.widget.Button
    private lateinit var tvMessage: android.widget.TextView
    private lateinit var tvAttempts: android.widget.TextView
    private lateinit var tvLeaderboard: android.widget.TextView
    private lateinit var tvTournamentPlayers: android.widget.TextView
    private lateinit var tvTournamentResults: android.widget.TextView
    private lateinit var tvHistory: android.widget.TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        initViews()

        api = Retrofit.Builder()
            .baseUrl("http://10.0.2.2:5000/")
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(GameApi::class.java)

        savedInstanceState?.let {
            currentPlayer = it.getString("PLAYER", "")
            currentAttempts = it.getInt("ATTEMPTS", 0)
            isGameWon = it.getBoolean("GAME_WON", false)
            etPlayer.setText(currentPlayer)
            updateGameState()
        }

        setupListeners()
        loadAllData()
    }

    private fun initViews() {
        etPlayer = findViewById(R.id.etPlayer)
        etGuess = findViewById(R.id.etGuess)
        btnAddTournament = findViewById(R.id.btnAddTournament)
        btnClearTournament = findViewById(R.id.btnClearTournament)
        btnStartGame = findViewById(R.id.btnStartGame)
        btnCheck = findViewById(R.id.btnCheck)
        tvMessage = findViewById(R.id.tvMessage)
        tvAttempts = findViewById(R.id.tvAttempts)
        tvLeaderboard = findViewById(R.id.tvLeaderboard)
        tvTournamentPlayers = findViewById(R.id.tvTournamentPlayers)
        tvTournamentResults = findViewById(R.id.tvTournamentResults)
        tvHistory = findViewById(R.id.tvHistory)
    }

    private fun setupListeners() {
        btnAddTournament.setOnClickListener { addToTournament() }
        btnClearTournament.setOnClickListener { clearTournament() }
        btnStartGame.setOnClickListener { startGame() }
        btnCheck.setOnClickListener { checkGuess() }
    }

    private fun startGame() {
        currentPlayer = etPlayer.text.toString().trim()
        if (currentPlayer.isEmpty()) {
            Toast.makeText(this, "Введіть ім'я!", Toast.LENGTH_SHORT).show()
            return
        }
        lifecycleScope.launch {
            try {
                val res = api.startGame()
                currentAttempts = 0
                isGameWon = false
                tvMessage.text = res.message
                etGuess.text.clear()
                btnCheck.isEnabled = true
                updateGameState()
            } catch (e: Exception) {
                showError(e)
            }
        }
    }

    private fun checkGuess() {
        val numStr = etGuess.text.toString().trim()
        if (numStr.isEmpty()) {
            Toast.makeText(this, "Введіть число!", Toast.LENGTH_SHORT).show()
            return
        }
        val guess = numStr.toIntOrNull() ?: run {
            Toast.makeText(this, "Тільки цифри!", Toast.LENGTH_SHORT).show()
            return
        }

        lifecycleScope.launch {
            try {
                val res = api.checkGuess(GuessRequest(guess, currentPlayer))
                currentAttempts = res.attempts
                tvMessage.text = res.result
                etGuess.text.clear()
                updateGameState()

                if (res.result == "Вгадав!") {
                    isGameWon = true
                    btnCheck.isEnabled = false
                    Toast.makeText(this@MainActivity, "🎉 Перемога!", Toast.LENGTH_LONG).show()
                    loadAllData()
                }
            } catch (e: Exception) {
                showError(e)
            }
        }
    }

    private fun addToTournament() {
        val p = etPlayer.text.toString().trim()
        if (p.isEmpty()) return Toast.makeText(this, "Введіть ім'я!", Toast.LENGTH_SHORT).show()

        lifecycleScope.launch {
            try {
                api.addToTournament(TournamentRequest(p))
                loadTournamentData()
            } catch (e: Exception) { showError(e) }
        }
    }

    private fun clearTournament() {
        lifecycleScope.launch {
            try {
                api.clearTournament()
                loadTournamentData()
            } catch (e: Exception) { showError(e) }
        }
    }

    private fun loadAllData() {
        loadLeaderboard()
        loadHistory()
        loadTournamentData()
    }

    private fun loadLeaderboard() {
        lifecycleScope.launch {
            try {
                val data = api.getLeaderboard()
                val text = data
                    .filter { it.player.isNotBlank() }
                    .joinToString("\n") {
                        "${it.player} — ${it.attempts} спроб"
                    }
                tvLeaderboard.text = "🏆 Лідерборд:\n$text"
            } catch (e: Exception) { showError(e) }
        }
    }

    private fun loadHistory() {
        lifecycleScope.launch {
            try {
                val data = api.getHistory()
                val text = data.joinToString("\n") { "${it.player} — ${it.attempts} — ${it.date}" }
                tvHistory.text = "📜 Історія матчів:\n$text"
            } catch (e: Exception) { showError(e) }
        }
    }

    private fun loadTournamentData() {
        lifecycleScope.launch {
            try {
                val players = api.getTournamentPlayers()
                val results = api.getTournamentResults()
                tvTournamentPlayers.text = "👥 Учасники турніру (${players.size}/8)\n${players.joinToString("\n") { "• $it" }}"
                tvTournamentResults.text = "🏅 Турнірна таблиця\n${results.joinToString("\n") { "${it.player} — ${it.attempts} спроб" }}"
            } catch (e: Exception) { showError(e) }
        }
    }

    private fun updateGameState() {
        tvAttempts.text = "Спроб: $currentAttempts"
        if (isGameWon) {
            btnCheck.isEnabled = false
            tvMessage.text = "🎉 Вітаємо, $currentPlayer! Ти переміг!"
        }
    }

    private fun showError(e: Exception) {
        runOnUiThread {
            val msg = if (e.message?.contains("failed to connect") == true)
                "⚠️ Сервер не запущено!" else "Помилка: ${e.message}"
            Toast.makeText(this, msg, Toast.LENGTH_LONG).show()
        }
    }

    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        outState.putString("PLAYER", currentPlayer)
        outState.putInt("ATTEMPTS", currentAttempts)
        outState.putBoolean("GAME_WON", isGameWon)
    }
}