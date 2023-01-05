import sqlite3
from datetime import datetime


def set_moving_data(user_id, date, text):
    with sqlite3.connect("users.db") as db:
        c = db.cursor()

        c.execute("""INSERT INTO materials_moving (user_id, local_datetime, moving, photos_list) 
        VALUES (?,?,?,NULL);""", (user_id, date, text))
        db.commit()


def update_photos_list(user_id, photos, date):
    with sqlite3.connect("users.db") as db:
        c = db.cursor()

        c.execute("""UPDATE materials_moving SET photos_list = ? WHERE user_id = ? and local_datetime = ?;""",
                  (photos, user_id, date))


def get_photos_list(user_id, date):
    with sqlite3.connect("users.db") as db:
        c = db.cursor()

        photos_list = c.execute("""SELECT photos_list FROM materials_moving 
        WHERE user_id = ? and local_datetime = ?;""", (user_id, date)).fetchone()[0]

    return photos_list


def get_moving_data(user_id, day=datetime.now().date()):
    with sqlite3.connect("users.db") as db:
        c = db.cursor()

        moving_data = c.execute("""SELECT local_datetime, moving, photos_list FROM materials_moving
        WHERE user_id = ? AND datetime(local_datetime).date() == ? ORDER BY datetime(local_datetime);""",
                                (user_id, day)).fetchall()
    return moving_data
