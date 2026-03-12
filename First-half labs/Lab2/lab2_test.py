from typing import List
import unittest
from lab2_guess_number import guess_number


def create_by_bounds(l: int, r: int) -> List[int]:
    """Создаёт список последовательных целых чисел от l до r включительно.

    Генерирует отсортированный список целых чисел, начиная с левой границы `l`
    и заканчивая правой границей `r` (включительно), с шагом 1.

    Args:
        l (int): Левая (начальная) граница диапазона.
        r (int): Правая (конечная) граница диапазона.

    Returns:
        List[int]: Список целых чисел от l до r включительно.
    """
    return [x for x in range(l, r + 1)]


class TestGuessNumber(unittest.TestCase):

    # Тесты через последовательный поиск

    def test_seq_found_first(self):
        """Элемент в начале"""
        self.assertEqual(guess_number(1, [3, 1, 2], "seq"), (1, 1))

    def test_seq_found_middle(self):
        """Элемент в середине."""
        self.assertEqual(guess_number(3, [5, 3, 1, 4, 2], "seq"), (3, 3))

    def test_seq_found_last(self):
        """Элемент найден в конце."""
        self.assertEqual(guess_number(5, [2, 5, 1, 3, 4], "seq"), (5, 5))

    def test_seq_not_found(self):
        """Элемент отсутствует."""
        self.assertEqual(guess_number(10, [1, 2, 3], "seq"), "Нет ответа (seq)")

    def test_seq_empty_list(self):
        """Пустой список."""
        self.assertEqual(guess_number(1, [], "seq"), "Нет ответа (seq)")

    # Тесты на бинарный поиск

    def test_bin_found_middle(self):
        """Элемент в середине """
        self.assertEqual(guess_number(3, create_by_bounds(1, 5), "bin"), (1, 3))

    def test_bin_found_first(self):
        """Элемент в начале"""
        self.assertEqual(guess_number(1, create_by_bounds(1, 5), "bin"), (3, 1))

    def test_bin_found_last(self):
        """Элемент в конце"""
        self.assertEqual(guess_number(5, create_by_bounds(1, 5), "bin"), (2, 5))

    def test_bin_not_found(self):
        """Элемент отсутствует."""
        self.assertEqual(guess_number(6, create_by_bounds(1, 5), "bin"), "Нет ответа (bin)")

    def test_bin_empty_list(self):
        """Пустой список."""
        self.assertEqual(guess_number(1, [], "bin"), "Нет ответа (bin)")

    def test_bin_unsorted_input(self):
        """Бинарный поиск на неотсортированном списке."""
        self.assertEqual(guess_number(3, [5, 1, 3, 2, 4], "bin"), (1, 3))

    def test_vanya_bin(self):
        """Тест Вани. Обычный."""
        self.assertEqual(guess_number(12, create_by_bounds(0, 16), "bin"), (4, 12))

    # Необычные случаи для системы

    def test_invalid_search_method(self):
        """Неверный метод поиска."""
        self.assertEqual(guess_number(1, [1, 2, 3], "abibibibibi"), "Ошибка типа поиска")

    def test_duplicates_seq(self):
        """Последовательный поиск при дубликатах — возвращает первый в списке."""
        self.assertEqual(guess_number(2, [3, 2, 1, 2, 4], "seq"), (2, 2))

    def test_duplicates_bin(self):
        """Бинарный поиск при дубликатах — находит одно из значений."""
        self.assertEqual(guess_number(2, [3, 2, 1, 2, 4], "bin"), (1, 2))


if __name__ == '__main__':
    unittest.main()

# Запуск тестов
if __name__ == '__main__':
    unittest.main()
