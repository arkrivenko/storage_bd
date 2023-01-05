import os
from dotenv import load_dotenv, find_dotenv
from telebot.types import BotCommand

if not find_dotenv():
    exit("Переменные окружения не загружены так как отсутствует файл .env")
else:
    load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
DEFAULT_COMMANDS = (
    ("/help", "Помощь"),
    ("/add_note", "Добавить запись"),
    ("/upload", "Выгрузить данные"),
    ("/history", "История движения ТМЦ")
)


def set_default_commands(bot):
    bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS]
    )
