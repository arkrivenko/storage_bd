import logging

from loader import bot
from pathlib import Path
from datetime import datetime
from database.database_functions import set_moving_data, get_photos_list, update_photos_list


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
            set_moving_data(message.from_user.id, local_datetime, moving_data)

            Path(f"files/{message.from_user.id}/{local_datetime.date()}/{local_datetime.time()}").mkdir(
                parents=True, exist_ok=True)

            msg = bot.send_message(message.from_user.id, f"Данные успешно сохранены: <b>{moving_data}</b>. "
                                                         f"Теперь необходимо загрузить фото.\n"
                                                         f"Для этого просто сделайте фотографию и "
                                                         f"отправьте в этот чат.", parse_mode="html")
            bot.register_next_step_handler(msg, photos_saver, local_datetime)

        except Exception:
            logging.exception("Возникла ошибка обработки введенных данных.")
            bot.send_message(message.from_user.id, "Что то пошло не так, попробуйте еще раз!")


def photos_saver(message, local_datetime):
    try:

        if not message.text:
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = f"files/{message.from_user.id}/{local_datetime.date()}/{local_datetime.time()}/" + \
                  file_info.file_path.replace("photos/", "")

            with open(src, "wb") as new_file:
                new_file.write(downloaded_file)

            photos_list = get_photos_list(message.from_user.id, local_datetime)

            if photos_list:
                updated_photos_list = " ".join([photos_list, src])
            else:
                updated_photos_list = src
            update_photos_list(message.from_user.id, updated_photos_list, local_datetime)

            msg = bot.send_message(message.from_user.id, "Если нужно добавить еще фото - просто загрузите сюда.")
            bot.register_next_step_handler(msg, photos_saver, local_datetime)

        else:
            bot.send_message(message.from_user.id, "Для создания новой записи нужно нажать /add_note")

    except Exception:
        logging.exception("Возникла ошибка записи фото.")
        bot.send_message(message.from_user.id, "Что то пошло не так, попробуйте отправить фото еще раз!")
