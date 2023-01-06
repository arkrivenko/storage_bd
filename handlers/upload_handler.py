import logging
from pathlib import Path
from loader import bot
from datetime import datetime
from database.database_functions import get_moving_data


@bot.message_handler(commands=["upload"])
def upload_func(message, another_day=None):
    try:
        if another_day:
            current_day = another_day
        else:
            current_day = datetime.now().date().strftime("%d-%m-%Y")

        path = f"./files/{message.from_user.id}/{current_day}"

        if not Path(path).is_dir():
            bot.send_message(message.from_user.id, f"Записи за {current_day} не найдены!")
        else:
            dirs = Path(path).iterdir()
            for i_dir in sorted(dirs, reverse=True):
                time = i_dir.name
                moving_data = get_moving_data(message.from_user.id, current_day, time)
                if not moving_data:
                    continue
                edited_moving_data = "\n".join(moving_data)
                bot.send_message(message.from_user.id, edited_moving_data)
                for photo in i_dir.iterdir():
                    bot.send_photo(message.from_user.id, open(str(photo), "rb"))

    except Exception:
        logging.exception("Ошибка вывода данных.")
        bot.send_message(message.from_user.id, "Что то пошло не так. Попробуйте еще раз!")
