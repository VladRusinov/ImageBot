import os

from dotenv import load_dotenv
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from handlers import image_handle, message_handle, wake_up

load_dotenv()

token = os.getenv('TOKEN')
if not token:
    raise ValueError("TOKEN is not set in the environment variables.")

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
