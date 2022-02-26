from flask import Flask, render_template, request, redirect, url_for
import datetime

app = Flask(__name__)

posts = []


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "GET":
        print(posts)
        return render_template("index.html", posts=posts)
    else:
        posts.append({"title": request.form["title"],
                          "text": request.form["text"],
                          "date": datetime.datetime.now(),
                          "time": datetime.datetime.now().strftime("%H:%M:%S"), })
        return redirect(url_for("index"))


@app.route("/new_note")
def new_note():
    return render_template("new_note.html")


@app.route("/notes")
def notes():
    return render_template("notes.html")


if __name__ == "__main__":
    app.run(debug=True)
