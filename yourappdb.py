import sqlite3
from flask import g

DATABASE = './database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def query_db(query, args=(), one=False):
    mydb = get_db()
    cur = mydb.execute(query, args)
    insert=""
    if "insert into" in query or ("update " in query and "set" in query):

        mydb.commit()
        insert="yes"

    rv = cur.fetchall()
    try:
        myid=cur.lastrowid
    except:
        myid=""
    cur.close()
    
    if insert == "yes":
        return {"myid": myid}
    else:
        return (rv[0] if rv else None) if one else rv
