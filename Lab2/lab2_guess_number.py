def seq_search(target:int, lst:list[int]) -> tuple[int, int] | str:
    """Последовательный поиск

    Ключевые аргументы:
        аналогичные функции guess_number

    Возвращает:
        Пара из количества попыток поиска и ответа, или же ошибку
    """
    check_am: int = 0

    # ищем число с помощью пробега по массиву
    for i in lst:
        check_am += 1
        if i == target:
            return check_am, i

    # если не нашлось -- возвращаем ошибку
    return "Нет ответа (seq)"

def bin_search(target:int, lst:list[int], check_am: int = 1) -> tuple[int, int] | str:
    """Бинарный поиск

    Ключевые аргументы:
        аналогичные функции guess_number

    Возвращает:
        Пара из количества попыток поиска и ответа, или же ошибку
    """
    r: int = len(lst)
    if r == 0:
        return "Нет ответа (bin)"
    if  target == lst[r // 2]:
        return check_am, lst[r // 2]
    elif target > lst[r // 2]:
        return bin_search(target, lst[r//2:], check_am + 1)
    else:
        return bin_search(target, lst[:r//2], check_am + 1)



def guess_number(target:int, lst:list[int], method='seq') -> tuple[int, int] | str:
    """Угадать число одним из двух способов

	Ключевые аргументы:
	    target -- int, число, которое нужно угадать
	    lst -- list[int], массив чисел, в котором происходит поиск (необязательно отсотированный)
	    method -- str, либо seq, либо bin -- последовательный или бинарный поиск.
	        по умолчанию последовательный, не требует обязательного написания

    Возвращает:
        Пара из количества попыток поиска и ответа, или же ошибку
	"""
    lst.sort()

    if method == 'seq':
        return seq_search(target, lst)
    elif method == 'bin':
        return bin_search(target, lst)
    else:
        return "Ошибка типа поиска"