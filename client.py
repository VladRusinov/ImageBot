import os
from io import BytesIO

from dotenv import load_dotenv
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from processor import ImageProcessor

load_dotenv()

token = os.getenv('TOKEN')


def message_handle(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='Отправьте мне изображение')


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    context.bot.send_message(
        chat_id=chat.id,
        text='Привет {}! отправь изображение, для выделения контуров'
        .format(name)
    )


def process_image(update, context):
    chat = update.effective_chat
    photo = update.message.photo
    if photo:
        file_id = photo[-1].file_id
        file = context.bot.get_file(file_id)
        file_stream = BytesIO()
        file.download(out=file_stream)
        file_stream.seek(0)
        image = ImageProcessor(file_stream)
        image.to_grayscale()
        image.apply_laplacian()
        result_img = image.convert_image_from_array()
        output_stream = BytesIO()
        result_img.save(output_stream, format="JPEG")
        output_stream.seek(0)
        context.bot.send_photo(chat_id=chat.id, photo=output_stream)


def main():
    updater = Updater(token=token)

    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(
        MessageHandler(Filters.photo, process_image)
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text, message_handle)
    )

    updater.start_polling()
    updater.idle()
