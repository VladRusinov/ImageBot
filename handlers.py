from io import BytesIO

from telegram.error import TelegramError

from processor import ImageProcessor
from logger_config import logger


def message_handle(update, context):
    """Обработка текстового сообщения."""
    try:
        chat = update.effective_chat
        context.bot.send_message(
            chat_id=chat.id,
            text='Отправьте мне изображение'
        )
    except TelegramError as error:
        logger.error(f'Не удалось отправить сообщение: {error}')
    else:
        logger.debug('Сообщение успешно отправлено')


def wake_up(update, context):
    """Обработка запуска бота."""
    try:
        chat = update.effective_chat
        name = update.message.chat.first_name
        context.bot.send_message(
            chat_id=chat.id,
            text=f'Привет {name}! Отправь изображение для выделения контуров.'
            .format(name)
        )
    except TelegramError as error:
        logger.error(f'Не удалось отправить сообщение: {error}')
    else:
        logger.debug('Сообщение успешно отправлено')


def image_handle(update, context):
    """Обработка изображения."""
    chat = update.effective_chat
    try:
        processing_msg = context.bot.send_message(
            chat_id=chat.id,
            text="⏳ Обрабатываю изображение, пожалуйста, подождите..."
        )
        photo = update.message.photo
        file_stream = download_image(context, photo[-1].file_id)
    except Exception as error:
        logger.error(
            f"Ошибка при загрузке изображения: {error}",
            exc_info=True
        )
        context.bot.send_message(
            chat_id=chat.id,
            text="Не удалось загрузить изображение."
        )
        return

    try:
        processed_image = process_image(file_stream)
        context.bot.delete_message(
            chat_id=chat.id,
            message_id=processing_msg.message_id
        )
        context.bot.send_photo(chat_id=chat.id, photo=processed_image)
    except Exception as error:
        logger.error(
            f"Ошибка при обработке изображения: {error}",
            exc_info=True
        )
        context.bot.delete_message(
            chat_id=chat.id,
            message_id=processing_msg.message_id
        )
        context.bot.send_message(
            chat_id=chat.id,
            text="Произошла ошибка при обработке изображения. Попробуйте снова"
        )
    else:
        logger.debug("Изображение успешно обработано и отправлено.")


def download_image(context, file_id):
    """Загрузка изображения."""
    file = context.bot.get_file(file_id)
    file_stream = BytesIO()
    file.download(out=file_stream)
    file_stream.seek(0)
    return file_stream


def process_image(file_stream):
    """Преобразование исходного изображения
    в изображение с выделенными контурами."""
    image = ImageProcessor(file_stream)
    image.to_grayscale()
    image.apply_laplacian()
    result_img = image.convert_image_from_array()
    output_stream = BytesIO()
    result_img.save(output_stream, format="JPEG")
    output_stream.seek(0)
    return output_stream
