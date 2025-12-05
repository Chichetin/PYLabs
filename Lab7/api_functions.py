import requests
import sys
import logging
from typing import Dict, List
from decorators import logger

console_logger = logging.getLogger("currency_console")
console_logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler(sys.stdout)
console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
console_logger.addHandler(console_handler)

@logger(handle=console_logger)
def get_currencies(
        currency_codes: List[str],
        url: str = "https://www.cbr-xml-daily.ru/daily_json.js"
) -> Dict[str, float]:
    """
    Получает курсы валют с API ЦБ РФ.

    Args:
        currency_codes: Список кодов валют (например, ['USD', 'EUR'])
        url: URL API ЦБ РФ

    Returns:
        Словарь {код_валюты: курс}

    Raises:
        ConnectionError: Если API недоступен
        ValueError: Если ответ невалидный JSON
        KeyError: Если в ответе нет ключа "Valute" или запрашиваемая валюта отсутствует
        TypeError: Если курс валюты имеет неверный тип (не число)
    """
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Failed to connect to {url}: {str(e)}")

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON response from {url}: {str(e)}")

    if "Valute" not in data:
        raise KeyError(f'Key "Valute" not found in API response. Available keys: {list(data.keys())}')

    valutes = data["Valute"]
    result = {}

    for code in currency_codes:
        code_upper = code.upper()

        if code_upper not in valutes:
            available = [key for key in valutes.keys() if key.isalpha()]
            raise KeyError(
                f'Currency "{code_upper}" not found. '
                f'Available currencies: {available}'
            )

        currency_data = valutes[code_upper]

        value = currency_data.get("Value")
        if not isinstance(value, (int, float)):
            raise TypeError(
                f'Currency "{code_upper}" has invalid rate type: '
                f'{type(value).__name__} (value: {value})'
            )

        result[code_upper] = float(value)

    return result