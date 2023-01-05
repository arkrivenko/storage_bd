from loader import bot
from config import set_default_commands
from database.database_init import db_create
import handlers


if __name__ == "__main__":
    db_create()
    set_default_commands(bot)
    bot.infinity_polling()
