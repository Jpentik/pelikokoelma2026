CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE games (
    id INTEGER PRIMARY KEY,
    description TEXT,
    platform TEXT,
    condition TEXT,
    user_id INTEGER REFERENCES users
);