package com.example.pz3

import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import com.example.pz3.MainActivity

class Level2Task7 {

    fun start(activity: MainActivity) {

        activity.setContentView(R.layout.activity_main)

        val etInput =
            activity.findViewById<EditText>(R.id.etInput)

        val btnAction =
            activity.findViewById<Button>(R.id.btnAction)

        val tvResult =
            activity.findViewById<TextView>(R.id.tvResult)

        btnAction.setOnClickListener {

            val guesses = etInput.text.toString()
                .split(" ")
                .mapNotNull { it.toIntOrNull() }

            if (guesses.size != 3) {

                tvResult.text =
                    "Введіть 3 числа"

                return@setOnClickListener
            }

            val cards = List(3) {
                (1..6).random()
            }

            var matches = 0

            for (g in guesses.distinct()) {

                if (g in cards) {
                    matches++
                }
            }

            tvResult.text =
                "Карти: $cards\n" +
                        "Ваші: $guesses\n" +
                        "Збігів: $matches"
        }
    }
}