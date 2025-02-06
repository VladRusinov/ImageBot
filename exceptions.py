class NoEnvVariablesError(Exception):
    """Исключение отсутствия переменных окружения."""

    def __init__(self, message=None):
        if message:
            self.message = message
        else:
            self.message = "Отсутсвуют переменные окружения"

    def __str__(self):
        return self.message
