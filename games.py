import sqlite3
import db

def add_game(content, user_id):
    db = sqlite3.connect("database.db")
    sql = """INSERT INTO games (content, user_id) VALUES (?, ?)"""
    db.execute(sql, [content, user_id])
    db.commit()
    db.close()

def get_games():
    sql = "SELECT id, content FROM games ORDER BY id DESC"
    return db.query(sql)

def get_game(game_id):
    sql = """SELECT games.id, games.content, users.username, users.id user_id
    FROM games, users
    WHERE games.user_id = users.id AND
    games.id = ?"""
    return db.query(sql, [game_id])[0]

def update_game(game_id, content):
    sql = """UPDATE games SET content = ? WHERE id = ?"""
    db.execute(sql, [content, game_id])