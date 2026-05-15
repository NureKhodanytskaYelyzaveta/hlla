package com.example.pz3

import android.widget.Button
import android.widget.EditText
import android.widget.TextView

class Level1Task7 {

    fun start(activity: MainActivity) {

        activity.setContentView(R.layout.activity_main)

        val etInput =
            activity.findViewById<EditText>(R.id.etInput)

        val btnAction =
            activity.findViewById<Button>(R.id.btnAction)

        val tvResult =
            activity.findViewById<TextView>(R.id.tvResult)

        btnAction.setOnClickListener {

            val month =
                etInput.text.toString().toIntOrNull()

            val result = when (month) {

                1 ->
                    "1 січня – Новий рік"

                2 ->
                    "14 лютого – День святого Валентина"

                3 ->
                    "8 березня – Міжнародний жіночий день"

                4 ->
                    "1 квітня - День дурня"

                5 ->
                    "1 травня – День праці"

                6 ->
                    "28 червня - День Конституції України"

                8 ->
                    "24 серпня – День Незалежності України"

                10 ->
                    "31 жовтня - Геловін"

                12 ->
                    "25 грудня - Різдво"

                else ->
                    "Свята не зазначені"
            }

            tvResult.text = result
        }
    }
}