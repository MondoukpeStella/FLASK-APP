import sqlite3
import click
from flask import current_app, g

def connect_db():
    g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
    g.db.row_factory = sqlite3.Row

def get_db():
    if 'db' not in g :
        connect_db()
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    
    if db is not None:
        db.close()
        
def init_db():
    db = get_db()
    
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    db.executescript("DROP TABLE IF EXISTS articles;")

    db.executescript("CREATE TABLE articles (id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT NOT NULL, body TEXT NOT NULL, creationDate date NOT NULL, userId INTEGER NOT NULL)")

    db.commit()
        
@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database')
    
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    
      