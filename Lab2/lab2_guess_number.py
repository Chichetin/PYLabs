from typing import List, Tuple


def seq_search(target: int, lst: List[int]) -> Tuple[int, int] | str:
    """Выполняет последовательный поиск целевого значения в списке.

    Args:
        target (int): Искомое целое число.
        lst (List[int]): Список целых чисел, в котором выполняется поиск.

    Returns:
        Tuple[int, int] | str:
            - Если элемент найден: кортеж из количества проверенных элементов
              и найденного значения.
            - Если элемент не найден: строка с сообщением об ошибке.
    """
    check_am: int = 0

    for i in lst:
        check_am += 1
        if i == target:
            return check_am, i

    return "Нет ответа (seq)"


def bin_search(
        target: int,
        lst: List[int],
        check_am: int = 1
) -> Tuple[int, int] | str:
    """Выполняет рекурсивный бинарный поиск целевого значения в отсортированном списке.

    Args:
        target (int): Искомое целое число.
        lst (List[int]): Отсортированный список целых чисел.
        check_am (int, optional): Текущее количество выполненных сравнений.
            По умолчанию 1.

    Returns:
        Tuple[int, int] | str:
            - Если элемент найден: кортеж из количества проверенных элементов
              и найденного значения.
            - Если элемент не найден: строка с сообщением об ошибке.
    """
    r: int = len(lst)

    if r == 0:
        return "Нет ответа (bin)"
    mid = r // 2
    if target == lst[mid]:
        return check_am, lst[mid]
    elif target > lst[mid]:
        return bin_search(target, lst[mid + 1:], check_am + 1)
    else:
        return bin_search(target, lst[:mid], check_am + 1)


def guess_number(
        target: int,
        lst: List[int],
        method: str = 'seq'
) -> Tuple[int, int] | str:
    """Осуществляет поиск целевого числа в списке с использованием указанного метода.

    Поддерживаемые методы: последовательный ('seq') и бинарный ('bin') поиск.
    Перед бинарным поиском список сортируется.

    Args:
        target (int): Искомое целое число.
        lst (List[int]): Список целых чисел.
        method (str, optional): Метод поиска. Допустимые значения:
            'seq' — последовательный поиск,
            'bin' — бинарный поиск.
            По умолчанию 'seq'.

    Returns:
        Tuple[int, int] | str:
            - Результат вызова соответствующей функции поиска.
            - При неверном указании метода — строка с сообщением об ошибке.
    """
    lst.sort()

    if method == 'seq':
        return seq_search(target, lst)
    elif method == 'bin':
        return bin_search(target, lst)
    else:
        return "Ошибка типа поиска"
