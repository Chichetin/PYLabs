import unittest
from gen_bin_tree import gen_bin_tree


class TestGenBinTree(unittest.TestCase):

    def test_height_1_returns_leaf(self):
        """Высота 1 — должен вернуться лист (пустой список потомков)."""
        result = gen_bin_tree(height=1, root=5)
        self.assertEqual(result, {"5": []})

    def test_height_2_default_functions(self):
        """Высота 2 с функциями по умолчанию: left = x*2, right = x+3."""
        result = gen_bin_tree(height=2, root=1)
        expected = {
            "1": [
                {"2": []},
                {"4": []}
            ]
        }
        self.assertEqual(result, expected)

    def test_height_3_default_functions(self):
        """Высота 3 с функциями по умолчанию — проверка рекурсивной структуры."""
        result = gen_bin_tree(height=3, root=1)
        expected = {
            "1": [
                {
                    "2": [
                        {"4": []},
                        {"5": []}
                    ]
                },
                {
                    "4": [
                        {"8": []},
                        {"7": []}
                    ]
                }
            ]
        }
        self.assertEqual(result, expected)

    def test_custom_left_and_right_functions(self):
        """Кастомные функции: left = x+1, right = x*3."""
        result = gen_bin_tree(
            height=2,
            root=2,
            l_b=lambda x: x + 1,
            r_b=lambda x: x * 3
        )
        expected = {
            "2": [
                {"3": []},
                {"6": []}
            ]
        }
        self.assertEqual(result, expected)

    def test_height_0_treated_as_leaf(self):
        """Высота <= 1 (включая 0) — всегда лист."""
        result = gen_bin_tree(height=0, root=10)
        self.assertEqual(result, {"10": []})

    def test_negative_height_returns_leaf(self):
        """Отрицательная высота — тоже лист."""
        result = gen_bin_tree(height=-5, root=7)
        self.assertEqual(result, {"7": []})

    def test_large_height_no_crash(self):
        """Большая высота (например, 5) — не вызывает ошибку и возвращает вложенную структуру."""
        result = gen_bin_tree(height=5, root=1)
        # Проверим, что структура существует и имеет нужную глубину
        self.assertIsInstance(result, dict)
        self.assertIn("1", result)
        self.assertEqual(len(result["1"]), 2)  # два поддерева

    def test_root_zero_with_default_functions(self):
        """Корень = 0 с функциями по умолчанию: left = 0*2 = 0, right = 0+3 = 3."""
        result = gen_bin_tree(height=2, root=0)
        expected = {
            "0": [
                {"0": []},
                {"3": []}
            ]
        }
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
