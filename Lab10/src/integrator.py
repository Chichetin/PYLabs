import math
from typing import Callable

def integrate(f: Callable[[float], float], a: float, b: float, *, n_iter: int = 100000) -> float:
    """
    Вычисляет определенный интеграл функции одной переменной методом прямоугольников.

    Назначение аргументов:
        f (Callable): Интегрируемая функция (принимает float, возвращает float).
        a (float): Нижний предел интегрирования.
        b (float): Верхний предел интегрирования.
        n_iter (int): Количество разбиений отрезка [a, b].
                      Чем выше значение, тем меньше погрешность.

    Возвращаемое значение:
        float: Приближенное значение интеграла.

    Ограничения:
        Метод левых прямоугольников имеет погрешность O(h).
        Функция f должна быть непрерывна на отрезке [a, b].

    Примеры (doctest):
    >>> # Интеграл cos(x) от 0 до pi/2 равен 1.0
    >>> round(integrate(math.cos, 0, math.pi / 2, n_iter=1000000), 5)
    1.0
    >>> # Интеграл x^2 от 0 до 3 равен 9.0
    >>> round(integrate(lambda x: x**2, 0, 3, n_iter=1000000), 2)
    9.0
    """
    acc: float = 0.0
    step: float = (b - a) / n_iter

    for i in range(n_iter):
        acc += f(a + i * step) * step

    return acc

if __name__ == "__main__":
    import doctest
    print("Запуск doctests...")
    doctest.testmod(verbose=True)