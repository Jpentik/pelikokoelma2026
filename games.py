import sqlite3

def add_game(content, user_id):
    db = sqlite3.connect("database.db")
    sql = """INSERT INTO games (content, user_id) VALUES (?, ?)"""
    db.execute(sql, [content, user_id])
    db.commit()
    db.close()