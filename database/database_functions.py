import sqlite3


def set_moving_data(user_id, date, time, text):
    with sqlite3.connect("users.db") as db:
        c = db.cursor()

        c.execute("""INSERT INTO materials_moving (user_id, local_date, local_time, moving) 
        VALUES (?,?,?,?);""", (user_id, date, time, text))
        db.commit()


def get_moving_data(user_id, date, time):
    with sqlite3.connect("users.db") as db:
        c = db.cursor()

        moving_data = c.execute("""SELECT local_date, local_time, moving FROM materials_moving WHERE user_id = ? AND 
        local_date == ? AND local_time == ?;""", (user_id, date, time)).fetchone()
    return moving_data
