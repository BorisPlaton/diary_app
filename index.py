from flask import Flask, render_template, request, redirect, url_for, g
import datetime
import sqlite3

app = Flask(__name__)


def connect_db():
    sql = sqlite3.connect("posts.db")
    sql.row_factory = sqlite3.Row
    return sql


def get_db():
    if not hasattr(g, "sqlite3"):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "sqlite_db"):
        g.sqlite_db.close()


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        return redirect(url_for("index"))


@app.route("/new_note")
def new_note():
    return render_template("new_note.html")


@app.route("/notes")
def notes():
    return render_template("notes.html")


if __name__ == "__main__":
    app.run(debug=True)
