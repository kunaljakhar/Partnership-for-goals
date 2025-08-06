import sqlite3

def initialize_db(db_path="app.db"):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, email TEXT, skills TEXT
    )''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, description TEXT, skill_tags TEXT
    )''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER, project_id INTEGER, similarity REAL
    )''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS negotiations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id INTEGER, expected_terms TEXT, proposed_terms TEXT, result_json TEXT
    )''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS communications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        negotiation_id INTEGER,
        message TEXT,
        tone_json TEXT
    )''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        negotiation_id INTEGER,
        doc_type TEXT,
        content TEXT,
        created_at TEXT
    )''')
    con.commit()
    con.close()

if __name__ == "__main__":
    initialize_db()
