# Лабораторная работа — Логирование и декораторы

**Автор:** Чичерин Александр Петрович
**Группа:** P3121

---

## Описание задачи

Реализовать параметризованный декоратор `@logger` для логирования вызовов функций с поддержкой различных `handle`:
- `sys.stdout` — вывод в консоль (по умолчанию)
- `io.StringIO` — вывод в строковый буфер
- `logging.Logger` — вывод через стандартный модуль логирования

Также реализовать функцию `get_currencies()` для получения курсов валют с API ЦБ РФ, которая должна:
- Содержать только бизнес-логику
- Выбрасывать конкретные исключения при ошибках
- Быть обернутой в декоратор `@logger`

---

## Структура файлов

| Файл                | Описание |
|---------------------|----------|
| `decorators.py`     | Реализация декоратора `logger` |
| `api_functions.py`  | Функция `get_currencies` с декоратором |
| `quadratic_demo.py` | Демонстрация с квадратным уравнением |
| `file_logging.py`   | Настройка файлового логирования |
| `tests.py`          | Полный набор тестов (unittest) |
| `README.md`         | Документация проекта |

---

## 1. Исходный код декоратора

```python
import sys
import logging
from functools import wraps
from typing import Union, Any, Callable

HandleType = Union[Any, logging.Logger]

def logger(func: Callable = None, *, handle: HandleType = sys.stdout) -> Callable:
    """Декоратор для логирования вызовов функций.
    
    Args:
        func: Функция для декорирования
        handle: Куда писать логи (sys.stdout, io.StringIO, logging.Logger)
    
    Returns:
        Обернутую функцию с логированием
    """
    if func is None:
        def decorator(actual_func: Callable) -> Callable:
            return logger(actual_func, handle=handle)
        return decorator

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        use_logging_module = isinstance(handle, logging.Logger)
        
        start_message = f"Starting function '{func.__name__}' with args={args}, kwargs={kwargs}"
        
        if use_logging_module:
            handle.info(start_message)
        else:
            handle.write(f"INFO: {start_message}\n")
            if hasattr(handle, 'flush'):
                handle.flush()
        
        try:
            result = func(*args, **kwargs)
            
            success_message = f"Function '{func.__name__}' returned: {result}"
            
            if use_logging_module:
                handle.info(success_message)
            else:
                handle.write(f"INFO: {success_message}\n")
                if hasattr(handle, 'flush'):
                    handle.flush()
            
            return result
            
        except Exception as e:
            error_message = f"Function '{func.__name__}' raised {type(e).__name__}: {str(e)}"
            
            if use_logging_module:
                handle.error(error_message)
            else:
                handle.write(f"ERROR: {error_message}\n")
                if hasattr(handle, 'flush'):
                    handle.flush()
            
            raise
    
    return wrapper
```

**Особенности реализации:**
- Поддержка трех способов вызова: `@logger`, `@logger()`, `@logger(handle=...)`
- Автоопределение типа `handle` через `isinstance(handle, logging.Logger)`
- Сохранение метаданных функции через `@functools.wraps`
- Поддержка как `logging.Logger`, так и любых объектов с методом `.write()`

---

## 2. Функция get_currencies

```python
import requests
from typing import Dict, List

def get_currencies(
    currency_codes: List[str],
    url: str = "https://www.cbr-xml-daily.ru/daily_json.js"
) -> Dict[str, float]:
    """
    Получает курсы валют с API ЦБ РФ.
    
    Args:
        currency_codes: Список кодов валют (например, ['USD', 'EUR'])
        url: URL API ЦБ РФ (можно подменить для тестирования)
    
    Returns:
        Словарь {код_валюты: курс}
    
    Raises:
        ConnectionError: Если API недоступен
        ValueError: Если ответ невалидный JSON
        KeyError: Если в ответе нет ключа "Valute" или запрашиваемая валюта отсутствует
        TypeError: Если курс валюты имеет неверный тип (не число)
    """
    # 1. Делаем запрос (может вызвать ConnectionError)
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Failed to connect to {url}: {str(e)}")
    
    # 2. Пробуем распарсить JSON (может вызвать ValueError)
    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON response from {url}: {str(e)}")
    
    # 3. Проверяем наличие ключа "Valute" (может вызвать KeyError)
    if "Valute" not in data:
        raise KeyError(f'Key "Valute" not found in API response')
    
    valutes = data["Valute"]
    result = {}
    
    # 4. Для каждой запрошенной валюты извлекаем курс
    for code in currency_codes:
        code_upper = code.upper()
        
        if code_upper not in valutes:
            raise KeyError(f'Currency "{code_upper}" not found in API response')
        
        currency_data = valutes[code_upper]
        value = currency_data.get("Value")
        
        if not isinstance(value, (int, float)):
            raise TypeError(f'Currency "{code_upper}" has invalid rate type: {type(value).__name__}')
        
        result[code_upper] = float(value)
    
    return result
```

**Обрабатываемые исключения:**

| Ситуация | Исключение | Описание |
|----------|------------|----------|
| API недоступен | `ConnectionError` | Проблемы с сетью или HTTP ошибки |
| Некорректный JSON | `ValueError` | Ответ не в формате JSON |
| Нет ключа "Valute" | `KeyError` | Неожиданная структура ответа API |
| Валюта отсутствует | `KeyError` | Запрошенной валюты нет в ответе |
| Неверный тип курса | `TypeError` | Курс не является числом |

---

## 3. Демонстрация работы с квадратным уравнением

```python
import math
import logging

@logger(handle=logging.getLogger("quadratic"))
def solve_quadratic(a: float, b: float, c: float):
    """
    Решает квадратное уравнение ax² + bx + c = 0.
    
    Returns:
        Корни уравнения или None если нет действительных корней
    
    Raises:
        ValueError: Некорректные коэффициенты
    """
    # Проверка типа данных
    if not all(isinstance(coef, (int, float)) for coef in (a, b, c)):
        raise ValueError("All coefficients must be numbers")
    
    # Невозможная ситуация (CRITICAL)
    if a == 0 and b == 0:
        logging.getLogger("quadratic").critical("Both a and b are zero - impossible equation")
        return None
    
    # Линейное уравнение
    if a == 0:
        return (-c / b,)
    
    # Квадратное уравнение
    D = b**2 - 4*a*c
    
    if D > 0:
        x1 = (-b + math.sqrt(D)) / (2*a)
        x2 = (-b - math.sqrt(D)) / (2*a)
        return (x1, x2)
    elif D == 0:
        x = -b / (2*a)
        return (x,)
    else:
        logging.getLogger("quadratic").warning("Discriminant is negative, no real roots")
        return None
```

**Уровни логирования для разных случаев:**

| Случай | Уровень логирования | Описание |
|--------|---------------------|----------|
| Успешное решение | INFO | Найдены корни уравнения |
| Дискриминант < 0 | WARNING | Нет действительных корней |
| Некорректные данные | ERROR | Коэффициенты не числа |
| a = b = 0 | CRITICAL | Невозможное уравнение |

---

## 4. Примеры логов

### Консольное логирование (sys.stdout):
```
INFO: Starting function 'get_currencies' with args=(['USD', 'EUR'],), kwargs={}
INFO: Function 'get_currencies' returned: {'USD': 93.25, 'EUR': 101.7}
```

### Логирование в StringIO:
```python
stream = io.StringIO()
@logger(handle=stream)
def test_func(x):
    return x * 2

result = test_func(5)
print(stream.getvalue())  # INFO: Starting function... INFO: Function returned...
```

### Логирование через модуль logging:
```
2024-01-15 10:30:00 - quadratic - INFO - Starting function 'solve_quadratic'
2024-01-15 10:30:00 - quadratic - WARNING - Discriminant is negative, no real roots
2024-01-15 10:31:00 - quadratic - ERROR - Function 'solve_quadratic' raised ValueError: All coefficients must be numbers
```

### Файловое логирование (currency_rates.log):
```
2024-01-15 10:32:00 - currency_file - INFO - Starting function 'get_currencies' with args=(['USD'],), kwargs={}
2024-01-15 10:32:01 - currency_file - INFO - Function 'get_currencies' returned: {'USD': 93.25}
```

---

## 5. Тестирование

### Тесты функции get_currencies

```python
class TestGetCurrenciesFunction(unittest.TestCase):
    def test_get_currencies_success(self):
        """Тест: успешное получение курсов валют."""
        with patch('api_functions.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {
                "Valute": {
                    "USD": {"Value": 90.5},
                    "EUR": {"Value": 98.7}
                }
            }
            mock_get.return_value = mock_response
            
            result = get_currencies(["USD", "EUR"])
            self.assertEqual(result, {"USD": 90.5, "EUR": 98.7})
    
    def test_get_currencies_nonexistent_currency(self):
        """Тест: запрос несуществующей валюты."""
        with patch('api_functions.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {
                "Valute": {"USD": {"Value": 90.5}}
            }
            mock_get.return_value = mock_response
            
            with self.assertRaises(KeyError):
                get_currencies(["XYZ"])
    
    def test_get_currencies_connection_error(self):
        """Тест: ошибка соединения с API."""
        with patch('api_functions.requests.get') as mock_get:
            mock_get.side_effect = ConnectionError("Network error")
            
            with self.assertRaises(ConnectionError):
                get_currencies(["USD"])
```

### Тесты декоратора

```python
class TestDecoratorWithStringIO(unittest.TestCase):
    def setUp(self):
        self.stream = io.StringIO()
        
        @logger(handle=self.stream)
        def wrapped():
            raise ConnectionError("Test connection error")
        
        self.wrapped = wrapped
    
    def test_logging_error(self):
        """Тест: логирование ошибки и проброс исключения."""
        with self.assertRaises(ConnectionError):
            self.wrapped()
        
        logs = self.stream.getvalue()
        self.assertIn("ERROR", logs)
        self.assertIn("ConnectionError", logs)
    
    def test_logging_success(self):
        """Тест: логирование успешного выполнения."""
        stream = io.StringIO()
        
        @logger(handle=stream)
        def add(a, b):
            return a + b
        
        result = add(3, 4)
        self.assertEqual(result, 7)
        
        logs = stream.getvalue()
        self.assertIn("Starting function 'add'", logs)
        self.assertIn("Function 'add' returned: 7", logs)
```

### Тесты квадратного уравнения

```python
class TestQuadraticEquation(unittest.TestCase):
    def test_two_roots(self):
        """Тест: уравнение с двумя корнями."""
        result = solve_quadratic(1, -3, 2)
        self.assertEqual(result, (2.0, 1.0))
    
    def test_no_real_roots(self):
        """Тест: уравнение без действительных корней."""
        result = solve_quadratic(1, 2, 5)
        self.assertIsNone(result)
    
    def test_invalid_coefficients(self):
        """Тест: некорректные коэффициенты."""
        with self.assertRaises(ValueError):
            solve_quadratic("a", 2, 3)
```

---

## 6. Результаты тестирования

```
Ran 15 tests in 0.156s

OK
```

| Группа тестов | Количество тестов | Статус |
|---------------|-------------------|--------|
| Декоратор `logger` | 5 | check  |
| Функция `get_currencies` | 6 | check  |
| Квадратное уравнение | 4 | check  |

---
