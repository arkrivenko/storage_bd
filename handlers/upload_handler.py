from pathlib import Path
from loader import bot
from datetime import datetime


@bot.message_handler(commands=["upload"])
def upload_func(message):
    path = Path(f"./files/{message.from_user.id}/{datetime.now().date()}")
    if not path.is_dir():
        bot.send_message(message.from_user.id, "Записи за текущий день не найдены!")
    else:
        dirs = path.iterdir()
        for dir in dirs:
            print(dir)
