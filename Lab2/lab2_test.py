import unittest
from lab2_guess_number import guess_number


def create_by_bounds(l: int, r: int):
    return [x for x in range(l, r + 1)]

class TestGuessNumber(unittest.TestCase):
    def test_no_answer(self):
        self.assertEqual(guess_number(2, [1, 2]), (2, 2))

    def test_no_answer_bin(self):
        self.assertEqual(guess_number(2, [1, 2], "bin"), (1, 2))

    def test_vanya_bin(self):
        self.assertEqual(guess_number(12, create_by_bounds(0, 16), "bin"), (2, 12))

    # NEED MORE TESTS

# Запуск тестов
if __name__ == '__main__':
    unittest.main()
