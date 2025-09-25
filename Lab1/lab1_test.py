import unittest
from main import two_sum


class TestTwoSum(unittest.TestCase):
    def test_add_zero(self):
        self.assertEqual(two_sum([2, 7, 11, 15], 9), [0, 1])

    def test_empty_lists(self):
        self.assertEqual(two_sum([], 1), "List format error")

    def test_string_in_nums(self):
        self.assertEqual(two_sum("2 3 5 7 9", 5), [0, 1])

    def test_string_in_target(self):
        self.assertEqual(two_sum([2, 3, 5, 7, 9], "5"), [0, 1])

    def test_good_floats(self):
        self.assertEqual(two_sum([5.0, 7.0, 6.0], 12), [0, 1])

    def test_many_answers(self):
        self.assertEqual(two_sum([3, 12, 5, 8, 96123123, 6], 11), "More than one answer")

    def test_wrong_target(self):
        self.assertEqual(two_sum([3, 12, 5, 8, 96123123, 6], "1s1"), "Target format error")

    def test_no_answer(self):
        self.assertEqual(two_sum([3000, 5000, 6000, 3, 5000, 501], "500"), "No answer")


# Запуск тестов
if __name__ == '__main__':
    unittest.main()
