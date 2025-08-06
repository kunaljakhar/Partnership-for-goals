import sqlite3
from datetime import datetime
import json

DB_PATH = "app.db"

def save_match(user_id, project_id, similarity):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO matches (user_id, project_id, similarity) VALUES (?, ?, ?)",
        (user_id, project_id, similarity))
    con.commit()
    match_id = cur.lastrowid
    con.close()
    return match_id

def save_negotiation(match_id, expected_terms, proposed_terms, result_json):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO negotiations (match_id, expected_terms, proposed_terms, result_json) VALUES (?, ?, ?, ?)",
        (match_id, json.dumps(expected_terms), json.dumps(proposed_terms), json.dumps(result_json)))
    con.commit()
    negotiation_id = cur.lastrowid
    con.close()
    return negotiation_id

def save_communication(negotiation_id, message, tone_json):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO communications (negotiation_id, message, tone_json) VALUES (?, ?, ?)",
        (negotiation_id, message, json.dumps(tone_json)))
    con.commit()
    comm_id = cur.lastrowid
    con.close()
    return comm_id

def save_document(negotiation_id, doc_type, content):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO documents (negotiation_id, doc_type, content, created_at) VALUES (?, ?, ?, ?)",
        (negotiation_id, doc_type, content, datetime.utcnow().isoformat()))
    con.commit()
    doc_id = cur.lastrowid
    con.close()
    return doc_id
