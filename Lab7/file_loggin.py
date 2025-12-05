# file_logging.py
import logging
from decorators import logger
from api_functions import get_currencies

file_logger = logging.getLogger("currency_file")
file_logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('currency_rates.log', mode='a', encoding='utf-8')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
file_logger.addHandler(file_handler)

# 3. Создаем новую версию функции, обернутую в декоратор с файловым логгером
# Важно: мы не меняем оригинальную get_currencies, а создаем новую обернутую версию
@logger(handle=file_logger)
def get_currencies_with_file_logging(currency_codes, url="https://www.cbr-xml-daily.ru/daily_json.js"):
    """
    Версия get_currencies с логированием в файл.
    Использует ту же бизнес-логику, но другой декоратор.
    """
    # Импортируем оригинальную НЕдекорированную функцию
    from api_functions import get_currencies as original_get_currencies
    return original_get_currencies(currency_codes, url)


if __name__ == "__main__":
    # Демонстрация работы
    print("Логирование курсов валют в файл 'currency_rates.log'...")

    try:
        # Используем версию с файловым логированием
        rates = get_currencies_with_file_logging(["USD", "EUR", "GBP"])
        print(f"Получены курсы: {rates}")
        print("Проверьте файл 'currency_rates.log'")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        print("Информация об ошибке записана в лог-файл")