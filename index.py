from flask import Flask, render_template, request, redirect, url_for
import datetime
import sqlite3


def rvs(mas: list):
    a = mas
    a.reverse()
    return a


app = Flask(__name__)


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
