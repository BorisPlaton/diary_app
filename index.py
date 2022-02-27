from flask import Flask, render_template, request, redirect, url_for, g
import datetime
import sqlite3

app = Flask(__name__)


def connect_db():
    sql = sqlite3.connect("post.db")
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


@app.route("/")
def index():
    db = get_db()
    cur = db.execute("""
    select * from post
    order by id desc;
    """)
    res = cur.fetchall()
    return render_template("index.html", posts=res)


@app.route("/new_note", methods=["GET", "POST"])
def new_note():
    if request.method == "GET":
        return render_template("new_note.html")
    else:
        now = datetime.datetime.now()

        post = request.form["text"]
        title = request.form["title"]
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")
        print(time, date)
        db = get_db()
        db.execute("""
            insert into post (post, title, date, time)
            values
                (?, ?, ?, ?);
        """, [post, title, date, time])
        db.commit()
        return redirect(url_for("index"))


@app.route("/notes")
def notes():
    return render_template("notes.html")


if __name__ == "__main__":
    app.run(debug=True)
