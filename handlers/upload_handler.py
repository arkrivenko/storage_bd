import logging
from pathlib import Path
from loader import bot
from datetime import datetime
from database.database_functions import get_moving_data


@bot.message_handler(commands=["upload"])
def upload_func(message):
    try:
        current_day = datetime.now().date().strftime("%d-%m-%Y")
        path = f"./files/{message.from_user.id}/{current_day}"
        if not Path(path).is_dir():
            bot.send_message(message.from_user.id, "Записи за текущий день не найдены!")
        else:
            dirs = Path(path).iterdir()
            for i_dir in sorted(dirs, reverse=True):
                print(f"i_dir: {i_dir}")
                time = str(i_dir).split("/")[-1]
                moving_data = get_moving_data(message.from_user.id, current_day, time)
                edited_moving_data = "\n".join(moving_data)
                bot.send_message(message.from_user.id, edited_moving_data)
                for photo in i_dir.iterdir():
                    bot.send_photo(message.from_user.id, open(str(photo), "rb"))

    except Exception:
        logging.exception("Ошибка вывода данных.")
        bot.send_message(message.from_user.id, "Что то пошло не так. Попробуйте еще раз!")
