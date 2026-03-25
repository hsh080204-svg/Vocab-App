from flask import Flask, render_template, request, redirect
from db import get_connection
import random

app = Flask(__name__)


@app.route("/")
def home():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM sections")
    sections = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("index.html", sections=sections)


@app.route("/add_section", methods=["POST"])
def add_section():

    name = request.form["name"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO sections (section_name) VALUES (%s)",
        (name,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/")

@app.route("/delete_section/<int:section_id>")
def delete_section(section_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM questions WHERE section_id=%s",
        (section_id,)
    )
    cursor.execute(
        "DELETE FROM sections WHERE section_id=%s",
        (section_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/")


@app.route("/section/<int:section_id>")
def show_section(section_id):

    return render_template(
        "section.html",
        section_id=section_id
    )


@app.route("/save_words", methods=["POST"])
def save_words():

    section_id = request.form["section_id"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM questions WHERE section_id=%s",
        (section_id,)
    )

    for i in range(1, 11):

        word = request.form.get(f"word{i}")
        meaning = request.form.get(f"meaning{i}")

        if word and meaning:

            cursor.execute(
                """
                INSERT INTO questions
                (section_id, word, meaning)
                VALUES (%s,%s,%s)
                """,
                (section_id, word, meaning)
            )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(f"/quiz/{section_id}")


@app.route("/quiz/<int:section_id>")
def quiz(section_id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT word, meaning FROM questions WHERE section_id=%s",
        (section_id,)
    )

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    words = rows.copy()
    meanings = rows.copy()

    random.shuffle(words)
    random.shuffle(meanings)

    return render_template(
        "quiz.html",
        words=words,
        meanings=meanings
    )

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
