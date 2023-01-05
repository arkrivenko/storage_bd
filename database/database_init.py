import sqlite3


def db_create():
    db = sqlite3.connect("users.db", check_same_thread=False)
    c = db.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS materials_moving(
    user_id INT,
    local_date TEXT,
    local_time TEXT,
    moving TEXT
    )""")

    db.commit()
    db.close()
