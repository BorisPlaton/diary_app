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


@app.route("/", methods=["GET", "POST" ])
def index():
    if request.method == "GET":
        db = get_db()
        cur = db.execute("""
            SELECT * FROM post
            ORDER BY id DESC;      
        """)
        res = cur.fetchall()
        return render_template("index.html", posts=res)
    else:
        db = get_db()
        db.execute("""
            DELETE FROM POST
            WHERE id = ?;
        """, [request.form["id"]])
        db.commit()
        return redirect(url_for("index"))


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
        db = get_db()
        db.execute("""
            INSERT INTO POST (post, title, date, time)
            VALUES
                (?, ?, ?, ?);
        """, [post, title, date, time])
        db.commit()
        return redirect(url_for("index"))


@app.route("/notes", methods=["POST", "GET"])
def notes():
    if request.method == "GET":
        db = get_db()
        cur = db.execute("""
            SELECT * FROM post
            ORDER BY date DESC;
        """)
        res = cur.fetchall()
        return render_template("notes.html", posts=res)
    else:
        if request.form["id"]:
            db = get_db()
            db.execute("""
                        DELETE FROM post
                        WHERE id = ?;
                    """, [request.form["id"]])
            db.commit()
            return redirect(url_for("notes"))
        else:
            db = get_db()
            title = request.form.get("title", "title")
            order = request.form.get("direction", "DESC")
            cur = db.execute(f"""
                        SELECT title, date
                        FROM post
                        WHERE title = ?
                        ORDER BY date {order};
                    """, [title])
            res = cur.fetchall()
            return render_template("notes.html", posts=res, method="GET")


if __name__ == "__main__":
    app.run(debug=True)
