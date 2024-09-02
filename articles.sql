DROP TABLE IF EXISTS articles;

CREATE TABLE articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    creationDate date NOT NULL,
    userId INTEGER NOT NULL
);