CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE games (
    id INTEGER PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users
);