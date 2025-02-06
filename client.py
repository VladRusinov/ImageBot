import os

from dotenv import load_dotenv
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from exceptions import NoEnvVariablesError
from handlers import image_handle, message_handle, wake_up
from logger_config import logger


load_dotenv()

token = os.getenv('TOKEN')
if not token:
    logger.critical('Отсутствуют переменные окружения')
    raise NoEnvVariablesError()

updater = Updater(token=token)

updater.dispatcher.add_handler(CommandHandler('start', wake_up))
updater.dispatcher.add_handler(
    MessageHandler(Filters.photo, image_handle)
)
updater.dispatcher.add_handler(
    MessageHandler(Filters.text, message_handle)
)

updater.start_polling()
updater.idle()
