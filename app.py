import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import db
import config
import games

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_games = games.get_games()
    return render_template("index.html", games=all_games)

@app.route("/find_game")
def find_game():
    query = request.args.get("query")
    if query:
        results = games.find_games(query)
    else:
        query = ""
        results = []
    return render_template("find_game.html", query=query, results=results)

@app.route("/game/<int:game_id>")
def show_game(game_id):
    game = games.get_game(game_id)
    if not game:
        abort(404)
    return render_template("show_game.html", game=game)

@app.route("/new")
def new():
    require_login()
    return render_template("new.html")

@app.route("/create_game", methods=["POST"])
def create_game():
    require_login()
    content = request.form["content"]
    user_id = session["user_id"]
    games.add_game(content, user_id)
    return redirect("/")

@app.route("/edit_game/<int:game_id>", methods=["GET", "POST"])
def edit_game(game_id):
    require_login()
    game = games.get_game(game_id)
    if not game:
        abort(404)
    if game["user_id"] != session["user_id"]:
        abort(403)
    return render_template("edit_game.html", game=game)

@app.route("/update_game", methods=["POST"])
def update_game():
    require_login()
    content = request.form["content"]
    game_id = request.form["game_id"]
    game = games.get_game(game_id)
    if not game:
        abort(404)
    if game["user_id"] != session["user_id"]:
        abort(403)
    games.update_game(game_id, content)
    return redirect("/game/" + str(game_id))

@app.route("/remove_game/<int:game_id>", methods=["GET", "POST"])
def remove_game(game_id):
    require_login()
    game = games.get_game(game_id)
    if not game:
        abort(404)
    if game["user_id"] != session["user_id"]:
        abort(403)
    if request.method == "GET":
        return render_template("remove_game.html", game=game)
    if request.method == "POST":
        if "remove" in request.form:
            games.remove_game(game_id)
            return redirect("/")
        else:
            return redirect("/game/" + str(game_id))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    if not username or len(username) < 4 or len(username) > 16:
        return render_template("username_length_error.html")
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if not password1 or len(password1) < 4 or len(password1) > 16:
        return render_template("password_length_error.html")
    if password1 != password2:
        return render_template("password_match_error.html")
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return render_template("username_taken_error.html")

    return render_template("user_created.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template(index.html)
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
    
        if not username or len(username) < 4 or len(username) > 16:
            return render_template("username_or_password_error.html")
        if not password or len(password) < 4 or len(password) > 16:
            return render_template("username_or_password_error.html")    
        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])[0]
        user_id = result["id"]
        password_hash = result["password_hash"]

    if check_password_hash(password_hash, password):
        session["user_id"] = user_id
        session["username"] = username
        return redirect("/")
    else:
        return render_template("username_or_password_error.html")

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")