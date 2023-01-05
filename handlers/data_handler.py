import logging

from loader import bot
from pathlib import Path
from datetime import datetime
from database.database_functions import set_moving_data


@bot.message_handler(commands=["add_note"])
def data_saver(message):
    msg = bot.send_message(message.from_user.id, f"Для создания новой записи продиктуйте в Gboard необходимое по "
                                                 f"следующему шаблону (выделенные ключевые слова проговариваем "
                                                 f"голосом):\n"
                                                 f"<b>Название</b> наименование товара <b>Накладная</b> номер накладной"
                                                 f" <b>Склад</b> номер склада", parse_mode="html")
    bot.register_next_step_handler(msg, text_parser)


def text_parser(message):
    flag = True
    word_keys = ("Название", "накладная", "склад")

    for word in word_keys:

        if word not in message.text:
            flag = False
            msg = bot.send_message(message.from_user.id, "Ключевые слова в тексте не найдены, попробуйте еще раз!")
            bot.register_next_step_handler(msg, text_parser)
            break

    if flag:
        try:
            text_list = message.text.split()
            name = text_list[1:text_list.index("накладная")]
            if len(name) > 1:
                name = " ".join(name)
            else:
                name = name[0]
            name = "Наименование товара: " + name

            document = text_list[text_list.index("накладная") + 1:text_list.index("склад")]
            document = "Номер накладной: " + "".join(document)

            warehouse = "Склад: " + text_list[-1]

            moving_data = '; '.join([name, document, warehouse])

            local_datetime = datetime.now()
            date = local_datetime.date().strftime("%d-%m-%Y")
            time = local_datetime.time().strftime("%H:%M:%S")
            set_moving_data(message.from_user.id, date, time, moving_data)

            Path(f"files/{message.from_user.id}/{date}/{time}").mkdir(
                parents=True, exist_ok=True)

            msg = bot.send_message(message.from_user.id, f"Данные успешно сохранены: <b>{moving_data}</b>. "
                                                         f"Теперь необходимо загрузить фото.\n"
                                                         f"Для этого просто сделайте фотографию и "
                                                         f"отправьте в этот чат.", parse_mode="html")
            bot.register_next_step_handler(msg, photos_saver, date, time)

        except Exception:
            logging.exception("Возникла ошибка обработки введенных данных.")
            bot.send_message(message.from_user.id, "Что то пошло не так, попробуйте еще раз!")


def photos_saver(message, date, time):
    try:

        if not message.text:
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = f"files/{message.from_user.id}/{date}/{time}/" + file_info.file_path.replace("photos/", "")

            with open(src, "wb") as new_file:
                new_file.write(downloaded_file)

            msg = bot.send_message(message.from_user.id, "Если нужно добавить еще фото - просто загрузите сюда.\n"
                                                         "Если фотографий больше не будет - "
                                                         "введите любой символ (например .)")
            bot.register_next_step_handler(msg, photos_saver, date, time)

    except Exception:
        logging.exception("Возникла ошибка записи фото.")
        msg = bot.send_message(message.from_user.id, "Что то пошло не так, попробуйте отправить фото еще раз!")
        bot.register_next_step_handler(msg, photos_saver, date, time)
