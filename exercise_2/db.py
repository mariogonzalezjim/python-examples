import sqlite3
import os
import json

def row_to_dict(cursor: sqlite3.Cursor, row: sqlite3.Row) -> dict:
    data = {}
    for idx, col in enumerate(cursor.description):
        data[col[0]] = row[idx]
    return data

def connect(db):
    conn = sqlite3.connect(db, check_same_thread=False)
    # return rows as json
    conn.row_factory = row_to_dict
    #by default, foreign_keys are disabled
    conn.execute("PRAGMA foreign_keys = 1")
    print("Database connected")
    return conn

def close(conn):
    conn.close()

def query(conn, query):
    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()

def querySingle(conn, query):
    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchone()

def insert(conn, query):
    try:
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        return cur.lastrowid
    except sqlite3.Error as e:
        return str(e)

def update(conn, query):
    try:
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        if cur.rowcount < 1:
            return "Update failed"
        else:
            return True
    except sqlite3.Error as e:
        return str(e)

def load_schema(schema, conn):
    with open(schema) as fp:
        conn.executescript(fp.read())
    print("Database schema imported")

def reset_db(db):
    if os.path.exists(db):
        os.remove(db)
        print("Database deleted")



