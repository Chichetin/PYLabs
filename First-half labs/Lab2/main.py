from typing import List
from lab2_guess_number import guess_number


def main() -> None:
    """Основная функция для взаимодействия с пользователем и запуска поиска числа.

    Позволяет пользователю выбрать способ задания списка:
    - вручную ввести элементы, или
    - задать диапазон (левая и правая границы).

    Затем запрашивает искомое число и метод поиска (линейный или бинарный),
    после чего вызывает функцию `guess_number` и выводит результат.
    """
    choice = input(
        "Хотите ввести весь массив вручную (0), или задать только границы (1)?\n"
    ).strip()

    lst: List[int]
    if choice == "1":
        left = int(input("Левая граница:\n"))
        right = int(input("Правая граница (невключительно):\n"))
        lst = list(range(left, right))
    else:
        user_input = input("Введите элементы массива через пробел:\n").strip()
        lst = list(map(int, user_input.split()))

    target = int(input("Введите искомое число:\n"))

    method_choice = input(
        "Введите способ поиска: 0 — линейный, 1 — бинарный\n"
    ).strip()
    method = "bin" if method_choice == "1" else "seq"

    result = guess_number(target, lst, method)
    print(result)


if __name__ == "__main__":
    main()
