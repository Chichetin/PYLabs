import sys
import logging
import math
from decorators import logger

demo_logger = logging.getLogger("quadratic_demo")
demo_logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(levelname)-8s - %(message)s')
console_handler.setFormatter(formatter)
demo_logger.addHandler(console_handler)

file_handler = logging.FileHandler('quadratic.log', mode='w', encoding='utf-8')
file_handler.setFormatter(formatter)
demo_logger.addHandler(file_handler)

@logger(handle=demo_logger)
def solve_quadratic(a: float, b: float, c: float):
    """
    Решает квадратное уравнение ax² + bx + c = 0.

    Returns:
        Кортеж (результат, уровень_логирования), где результат:
        - (x1, x2) для D > 0
        - x для D = 0
        - None для D < 0
        - Исключение при ошибке

    Raises:
        ValueError: Некорректные коэффициенты
    """
    # Проверка на "невозможную" ситуацию (CRITICAL)
    if a == 0 and b == 0:
        # Возвращаем результат и уровень логирования
        return None, logging.CRITICAL

    # Проверка типа данных (ERROR)
    if not all(isinstance(coef, (int, float)) for coef in (a, b, c)):
        raise ValueError("All coefficients must be numbers")

    # Случай линейного уравнения
    if a == 0:
        if b == 0:
            return None, logging.CRITICAL
        x = -c / b
        return (x,), logging.INFO

    # Вычисляем дискриминант
    D = b**2 - 4*a*c

    if D > 0:
        # Два корня
        x1 = (-b + math.sqrt(D)) / (2*a)
        x2 = (-b - math.sqrt(D)) / (2*a)
        return (x1, x2), logging.INFO

    elif D == 0:
        # Один корень
        x = -b / (2*a)
        return (x,), logging.INFO

    else:
        # Нет действительных корней
        return None, logging.WARNING

def demonstrate():
    """Демонстрация работы функции с разными случаями."""
    print("=" * 60)
    print("ДЕМОНСТРАЦИЯ: Решение квадратных уравнений с логированием")
    print("=" * 60)

    test_cases = [
        # (a, b, c, описание)
        (1, -3, 2, "D > 0: два корня (x² - 3x + 2 = 0)"),
        (1, -2, 1, "D = 0: один корень (x² - 2x + 1 = 0)"),
        (1, 2, 5, "D < 0: нет действительных корней (x² + 2x + 5 = 0)"),
        (0, 2, -4, "Линейное уравнение (2x - 4 = 0)"),
        (0, 0, 5, "CRITICAL: оба коэффициента равны 0 (0x² + 0x + 5 = 0)"),
    ]

    for a, b, c, description in test_cases:
        print(f"\n{'='*40}")
        print(f"Тест: {description}")
        print(f"Коэффициенты: a={a}, b={b}, c={c}")
        print("-" * 40)

        try:
            result = solve_quadratic(a, b, c)
            if result is not None:
                print(f"Результат: {result}")
            else:
                print("Результат: None (нет действительных корней)")
        except Exception as e:
            print(f"Исключение: {type(e).__name__}: {e}")

    print(f"\n{'='*60}")
    print("Демонстрация с некорректными данными (ERROR):")
    print("-" * 60)

    try:
        # Вызов с некорректными типами
        solve_quadratic("abc", 2, 3)
    except ValueError as e:
        print(f"Поймано исключение: {e}")

    print(f"\n{'='*60}")
    print("Проверьте также файл 'quadratic.log'")
    print("=" * 60)

if __name__ == "__main__":
    demonstrate()