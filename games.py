import sqlite3
import db

def add_game(description, platform, condition, user_id):
    sql = """INSERT INTO games (description, platform, condition, user_id) VALUES (?, ?, ?, ?)"""
    db.execute(sql, [description, platform, condition, user_id])

def get_games():
    sql = "SELECT id, description FROM games ORDER BY id DESC"
    return db.query(sql)

def get_game(game_id):
    sql = """SELECT games.id, 
                    games.description, 
                    users.username, 
                    users.id user_id
                    FROM games, users
                    WHERE games.user_id = users.id AND
                    games.id = ?"""
    result = db.query(sql, [game_id])
    return result[0] if result else None

def update_game(game_id, description):
    sql = "UPDATE games SET description = ? WHERE id = ?"
    db.execute(sql, [description, game_id])

def remove_game(game_id):
    sql = "DELETE FROM games  WHERE id = ?"
    db.execute(sql, [game_id])

def find_games(query):
    sql = """SELECT id, description
    FROM games
    WHERE description LIKE ?
    ORDER BY id DESC"""
    return db.query(sql, ["%" + query + "%"])