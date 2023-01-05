from loader import bot


@bot.message_handler(commands=["start", "help"])
def start_message(message):
    bot.send_message(message.from_user.id, f"Добро пожаловать, <b>{message.from_user.full_name}</b>.\n"
                                           f"Вас приветствует бот для записи перемещений ТМЦ Вашей организации.\n"
                                           f"Для создания новой записи нажмите на /add_note\n"
                                           f"Для выгрузки сохраненных данных в файл нажмите /upload\n", parse_mode="html")
