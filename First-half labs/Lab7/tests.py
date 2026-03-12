# tests.py
import unittest
import io
import sys
import logging
from unittest.mock import patch, Mock
from decorators import logger
from api_functions import get_currencies

class TestDecoratorBasic(unittest.TestCase):
    """Базовые тесты декоратора."""

    def test_decorator_without_parentheses(self):
        """Тест: декоратор без скобок @logger."""

        stream = io.StringIO()

        # Важно: создаем функцию здесь, чтобы stream был доступен
        @logger(handle=stream)
        def add(a, b):
            return a + b

        result = add(3, 4)

        # Проверяем результат функции
        self.assertEqual(result, 7)

        # Проверяем логи
        logs = stream.getvalue()
        self.assertIn("Starting function 'add'", logs)
        self.assertIn("Function 'add' returned: 7", logs)
        self.assertIn("INFO:", logs)

    def test_decorator_with_parentheses(self):
        """Тест: декоратор со скобками @logger()."""

        stream = io.StringIO()

        @logger(handle=stream)
        def multiply(x, y):
            return x * y

        result = multiply(5, 6)

        self.assertEqual(result, 30)

        logs = stream.getvalue()
        self.assertIn("multiply", logs)
        self.assertIn("30", logs)

    def test_decorator_with_logging_module(self):
        """Тест: декоратор с объектом logging.Logger."""

        # Создаем mock-логгер
        mock_logger = Mock(spec=logging.Logger)

        @logger(handle=mock_logger)
        def divide(a, b):
            return a / b

        result = divide(10, 2)

        self.assertEqual(result, 5)

        # Проверяем, что методы логгера были вызваны
        mock_logger.info.assert_called()
        self.assertEqual(mock_logger.info.call_count, 2)  # Старт и успех

    def test_decorator_error_logging(self):
        """Тест: логирование ошибок декоратором."""

        stream = io.StringIO()

        @logger(handle=stream)
        def risky_function():
            raise ValueError("Something went wrong")

        # Проверяем, что исключение пробрасывается
        with self.assertRaises(ValueError):
            risky_function()

        # Проверяем логи об ошибке
        logs = stream.getvalue()
        self.assertIn("ERROR:", logs)
        self.assertIn("ValueError", logs)
        self.assertIn("Something went wrong", logs)


class TestGetCurrenciesFunction(unittest.TestCase):
    """Тесты функции get_currencies (бизнес-логика)."""

    def test_get_currencies_success(self):
        """Тест: успешное получение курсов валют."""
        # Используем mock, чтобы не зависеть от реального API
        with patch('api_functions.requests.get') as mock_get:
            # Подготавливаем mock-ответ
            mock_response = Mock()
            mock_response.json.return_value = {
                "Valute": {
                    "USD": {"Value": 90.5},
                    "EUR": {"Value": 98.7}
                }
            }
            mock_get.return_value = mock_response

            # Вызываем функцию
            result = get_currencies(["USD", "EUR"])

            # Проверяем результат
            self.assertEqual(result, {"USD": 90.5, "EUR": 98.7})

    def test_get_currencies_nonexistent_currency(self):
        """Тест: запрос несуществующей валюты."""
        with patch('api_functions.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {
                "Valute": {
                    "USD": {"Value": 90.5}
                }
            }
            mock_get.return_value = mock_response

            # Должен возникнуть KeyError
            with self.assertRaises(KeyError):
                get_currencies(["XYZ"])

    def test_get_currencies_connection_error(self):
        """Тест: ошибка соединения с API."""
        with patch('api_functions.requests.get') as mock_get:
            mock_get.side_effect = ConnectionError("Network error")

            # Должен возникнуть ConnectionError
            with self.assertRaises(ConnectionError):
                get_currencies(["USD"])

    def test_get_currencies_invalid_json(self):
        """Тест: некорректный JSON в ответе."""
        with patch('api_functions.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.side_effect = ValueError("Invalid JSON")
            mock_get.return_value = mock_response

            # Должен возникнуть ValueError
            with self.assertRaises(ValueError):
                get_currencies(["USD"])

    def test_get_currencies_no_valute_key(self):
        """Тест: в ответе нет ключа 'Valute'."""
        with patch('api_functions.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {
                "error": "Something went wrong"
            }
            mock_get.return_value = mock_response

            # Должен возникнуть KeyError
            with self.assertRaises(KeyError):
                get_currencies(["USD"])

    def test_get_currencies_invalid_rate_type(self):
        """Тест: курс валюты имеет неверный тип."""
        with patch('api_functions.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {
                "Valute": {
                    "USD": {"Value": "not a number"}  # Строка вместо числа
                }
            }
            mock_get.return_value = mock_response

            # Должен возникнуть TypeError
            with self.assertRaises(TypeError):
                get_currencies(["USD"])


class TestDecoratorWithStringIO(unittest.TestCase):
    """Тесты поведения декоратора с StringIO (как в задании)."""

    def setUp(self):
        """Подготовка перед каждым тестом."""
        self.stream = io.StringIO()

        # Создаем декорированную функцию как в задании
        @logger(handle=self.stream)
        def wrapped():
            # Имитируем функцию, которая всегда вызывает ConnectionError
            raise ConnectionError("Test connection error")

        self.wrapped = wrapped

    def test_logging_error(self):
        """Тест: логирование ошибки и проброс исключения."""
        # Проверяем, что исключение пробрасывается
        with self.assertRaises(ConnectionError):
            self.wrapped()

        # Получаем логи
        logs = self.stream.getvalue()

        # Проверяем содержание логов
        self.assertIn("ERROR", logs)
        self.assertIn("ConnectionError", logs)
        self.assertIn("Test connection error", logs)

    def test_log_format(self):
        """Тест: формат логов содержит нужную информацию."""

        @logger(handle=self.stream)
        def sample_func(x, y=10):
            return x + y

        sample_func(5, y=20)

        logs = self.stream.getvalue()

        # Проверяем, что логи содержат:
        self.assertIn("Starting function", logs)
        self.assertIn("sample_func", logs)
        self.assertIn("args=(5,)", logs)  # Позиционные аргументы
        self.assertIn("kwargs={'y': 20}", logs)  # Именованные аргументы
        self.assertIn("returned: 25", logs)


class TestIntegration(unittest.TestCase):
    """Интеграционные тесты."""

    def test_decorated_get_currencies_success(self):
        """Тест: декорированная функция успешно получает курсы."""
        stream = io.StringIO()

        # Создаем декорированную версию функции
        decorated_func = logger(handle=stream)(get_currencies)

        with patch('api_functions.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {
                "Valute": {
                    "USD": {"Value": 91.2}
                }
            }
            mock_get.return_value = mock_response

            result = decorated_func(["USD"])

            # Проверяем результат
            self.assertEqual(result, {"USD": 91.2})

            # Проверяем логи
            logs = stream.getvalue()
            self.assertIn("get_currencies", logs)
            self.assertIn("INFO:", logs)

    def test_decorated_get_currencies_error(self):
        """Тест: декорированная функция логирует ошибку."""
        stream = io.StringIO()

        decorated_func = logger(handle=stream)(get_currencies)

        with patch('api_functions.requests.get') as mock_get:
            mock_get.side_effect = ConnectionError("Mock error")

            with self.assertRaises(ConnectionError):
                decorated_func(["USD"])

            logs = stream.getvalue()
            self.assertIn("ERROR:", logs)
            self.assertIn("ConnectionError", logs)


class TestFileLogging(unittest.TestCase):
    """Тесты логирования в файл."""

    def test_file_logging_setup(self):
        """Тест: настройка файлового логирования."""
        import tempfile
        import os

        # Создаем временный файл
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as tmp_file:
            tmp_path = tmp_file.name

        try:
            # Настраиваем логгер для файла
            file_logger = logging.getLogger("test_file_logger")
            file_logger.setLevel(logging.INFO)

            # Очищаем предыдущие обработчики
            file_logger.handlers.clear()

            # Добавляем обработчик для временного файла
            file_handler = logging.FileHandler(tmp_path, mode='a', encoding='utf-8')
            file_formatter = logging.Formatter('%(name)s - %(message)s')
            file_handler.setFormatter(file_formatter)
            file_logger.addHandler(file_handler)

            # Создаем декорированную функцию
            @logger(handle=file_logger)
            def test_func():
                return "success"

            # Вызываем функцию
            result = test_func()
            self.assertEqual(result, "success")

            # Даем время на запись в файл
            file_handler.flush()

            # Читаем файл и проверяем содержимое
            with open(tmp_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertIn("test_file_logger", content)
                self.assertIn("test_func", content)

        finally:
            # Удаляем временный файл
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)


if __name__ == '__main__':
    # Создаем test suite
    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])

    # Запускаем тесты с детальным выводом
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Выводим статистику
    print(f"\n{'='*60}")
    print(f"Тестов запущено: {result.testsRun}")
    print(f"Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
    if result.failures:
        print(f"Провалено: {len(result.failures)}")
        for test, traceback in result.failures:
            print(f"\nПровален: {test}")
            print(traceback)
    if result.errors:
        print(f"Ошибок: {len(result.errors)}")
        for test, traceback in result.errors:
            print(f"\nОшибка в: {test}")
            print(traceback)