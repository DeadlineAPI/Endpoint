import sqlite3
import os

defaultentry = dict(
    name=None,
    shortname=None,
    cycle=None,
    confurl=None,
    cfpurl=None,
    categories=None,
    logourl=None,
    location_virtual=None,
    location_country=None,
    location_city=None,
    location_lat=None,
    location_lon=None,
    startdate=None,
    enddate=None,
    deadline=None,
    pagelimit=None
)

def get_db(path='endpoint.db'):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Verify that the db is the correct version and set up
    tables = cur.execute("SELECT * FROM sqlite_schema where type='table' AND name NOT LIKE 'sqlite_%' ")
    for table in tables.fetchall():
        if table["name"] == "entries":
            return conn

    _initialize_database(conn)
    return conn

def reset_database(path='endpoint.db'):
    os.remove(path)
    conn = sqlite3.connect(path)
    _initialize_database(conn)
    conn.close()

def _initialize_database(conn):
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE entries(
        id INTEGER PRIMARY KEY ASC, 
        name TEXT NOT NULL, 
        shortname TEXT,
        cycle TEXT,
        confurl TEXT,
        cfpurl TEXT,
        categories TEXT,
        location_virtual INTEGER,
        location_country TEXT,
        location_city TEXT,
        location_lat TEXT,
        location_lon TEXT,
        startdate TEXT,
        enddate TEXT,
        deadline TEXT NOT NULL,
        pagelimit TEXT,
        logourl TEXT
        )
                """)

def get_entries(conn):
    cur = conn.cursor()
    res = cur.execute("SELECT * FROM entries")
    return res.fetchall()

def get_entry(conn, id):
    cur = conn.cursor()
    res = cur.execute("SELECT * FROM entries WHERE id=?", str(id))
    return res.fetchone()

def delete_entry(conn, id):
    cur = conn.cursor()
    res = cur.execute("DELETE FROM entries WHERE id=?", str(id))
    conn.commit()
    return res

def edit_entry(conn, entry, id):
    cur = conn.cursor()

    keys = defaultentry.keys()
    values = tuple([entry[key] for key in defaultentry])

    string = ','.join([f"{k}=\"{v}\"" if v is not None else f"{k}=null" for k,v in zip(keys,values)])
    print("UPDATE users SET "+string+" WHERE id=?")
    res = cur.execute("UPDATE entries SET "+string+" WHERE id=?", str(id))
    conn.commit()
    return res

def get_entries_with_future_deadline(conn):
    cur = conn.cursor()
    pass

def get_entries_with_future_enddate(conn):
    cur = conn.cursor()
    pass

def add_entry(conn, e):
    cur = conn.cursor()

    print(e)
    assert "name" in e
    assert "deadline" in e
    assert "startdate" in e
    assert "deadline" in e



    e = { **defaultentry, **e }

    keys = ','.join(defaultentry.keys())
    question_marks = ','.join(list('?'*len(defaultentry)))
    values = tuple([e[key] for key in defaultentry])

    res = cur.execute('INSERT INTO entries ('+keys+') VALUES ('+question_marks+')', values)
    conn.commit()

