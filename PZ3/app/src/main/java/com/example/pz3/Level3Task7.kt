package com.example.pz3

import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import java.io.File

class Level3Task7 {

    fun start(activity: MainActivity) {

        activity.setContentView(R.layout.activity_main)

        val etInput =
            activity.findViewById<EditText>(R.id.etInput)

        val btnAction =
            activity.findViewById<Button>(R.id.btnAction)

        val tvResult =
            activity.findViewById<TextView>(R.id.tvResult)

        btnAction.setOnClickListener {

            try {

                val file =
                    File(activity.filesDir, "text.txt")

                file.writeText(
                    etInput.text.toString()
                )

                var letters = 0
                var spaces = 0
                var signs = 0

                for (c in file.readText()) {

                    when {

                        c.isLetter() -> letters++

                        c.isWhitespace() -> spaces++

                        else -> signs++
                    }
                }

                val result =
                    "Літер: $letters\n" +
                            "Пробілів: $spaces\n" +
                            "Знаків: $signs"

                tvResult.text = result

            } catch (e: Exception) {

                tvResult.text =
                    "Помилка: ${e.message}"
            }
        }
    }
}