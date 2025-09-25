import unittest
from main import two_sum


class TestTwoSum(unittest.TestCase):

    def test_add_zero(self):
        self.assertEqual(two_sum([2,7,11,15], 9), [0, 1])

# Запуск тестов
if __name__ == '__main__':
    unittest.main()
