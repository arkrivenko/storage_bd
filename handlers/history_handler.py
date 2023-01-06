import logging

from loader import bot
from datetime import datetime
from handlers.upload_handler import upload_func


@bot.message_handler(commands=["history"])
def history_func(message):
    msg = bot.send_message(message.from_user.id, "Введите дату в следующем формате: \n"
                                                 "<b>день.месяц.год</b>", parse_mode="html")
    bot.register_next_step_handler(msg, date_check)


def date_check(message):
    date = message.text
    try:
        valid_date = datetime.strptime(date, "%d.%m.%Y")
        date_to_load = valid_date.strftime("%d-%m-%Y")
        upload_func(message, date_to_load)

    except Exception:
        logging.exception("Ошибка при вывода истории перемещений")
        msg = bot.send_message(message.from_user.id, "Что то пошло не так, попробуйте ввести дату еще раз!\n"
                                                     "<b>день.месяц.год</b>", parse_mode="html")
        bot.register_next_step_handler(msg, date_check)

