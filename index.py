from flask import Flask, render_template
import datetime

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/notes")
def notes():
    return render_template("notes.html")


if __name__ == "__main__":
    app.run(debug=True)
