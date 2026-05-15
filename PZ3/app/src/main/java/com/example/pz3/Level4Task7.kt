package com.example.pz3

import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import java.io.File

class Level4Task7 {

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

                val text =
                    etInput.text.toString()

                val file =
                    File(activity.filesDir, "source.txt")

                file.writeText(text)

                val shift = 3

                var encrypted = ""

                for (ch in text) {

                    if (ch in 'a'..'z') {

                        encrypted +=
                            ((ch.code - 'a'.code + shift) % 26 + 'a'.code).toChar()

                    } else if (ch in 'A'..'Z') {

                        encrypted +=
                            ((ch.code - 'A'.code + shift) % 26 + 'A'.code).toChar()

                    } else {

                        encrypted += ch
                    }
                }

                var decrypted = ""

                for (ch in encrypted) {

                    if (ch in 'a'..'z') {

                        decrypted +=
                            ((ch.code - 'a'.code - shift + 26) % 26 + 'a'.code).toChar()

                    } else if (ch in 'A'..'Z') {

                        decrypted +=
                            ((ch.code - 'A'.code - shift + 26) % 26 + 'A'.code).toChar()

                    } else {

                        decrypted += ch
                    }
                }

                tvResult.text =
                    "Оригінал:\n$text\n\n" +
                            "Шифр:\n$encrypted\n\n" +
                            "Дешифрування:\n$decrypted"

            } catch (e: Exception) {

                tvResult.text =
                    "Помилка:\n${e.message}"
            }
        }
    }
}