from io import BytesIO

from processor import ImageProcessor


def message_handle(update, context):
    """Обработка текстового сообщения."""
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='Отправьте мне изображение')


def wake_up(update, context):
    """Обработка запуска бота."""
    chat = update.effective_chat
    name = update.message.chat.first_name
    context.bot.send_message(
        chat_id=chat.id,
        text='Привет {}! отправь изображение, для выделения контуров'
        .format(name)
    )


def image_handle(update, context):
    """Обработка изображения."""
    chat = update.effective_chat
    try:
        photo = update.message.photo
        file_stream = download_image(context, photo[-1].file_id)
        processed_image = process_image(file_stream)
        context.bot.send_photo(chat_id=chat.id, photo=processed_image)
    except Exception:
        context.bot.send_message(
            chat_id=chat.id,
            text="Произошла ошибка при обработке вашего запроса."
        )


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
