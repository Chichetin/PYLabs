import unittest
from binary_tree import gen_bin_tree


class TestGenBinTree(unittest.TestCase):
    """Класс тестов для функции gen_bin_tree."""

    def test_default_parameters_variant_18(self):
        """Тест с параметрами по умолчанию (вариант 18)."""
        tree = gen_bin_tree()

        self.assertIn(18, tree)
        self.assertEqual(tree[18], [30, 52])
        self.assertIn(30, tree)
        self.assertIn(52, tree)
        self.assertEqual(len(tree), 31)

    def test_custom_height(self):
        """Тест с пользовательской высотой."""
        tree = gen_bin_tree(height=1)
        self.assertEqual(len(tree), 1)
        self.assertEqual(tree[18], [None, None])

        tree = gen_bin_tree(height=2)
        self.assertEqual(len(tree), 3)
        self.assertEqual(tree[18], [30, 52])
        self.assertEqual(tree[30], [None, None])
        self.assertEqual(tree[52], [None, None])

    def test_custom_root_and_formulas(self):
        """Тест с полностью пользовательскими параметрами."""
        tree = gen_bin_tree(
            height=3,
            root=5,
            left_branch=lambda x: x + 1,
            right_branch=lambda x: x * 2,
        )

        self.assertEqual(tree[5], [6, 10])
        self.assertEqual(tree[6], [7, 12])
        self.assertEqual(tree[10], [11, 20])
        self.assertEqual(tree[7], [None, None])
        self.assertEqual(tree[12], [None, None])
        self.assertEqual(tree[11], [None, None])
        self.assertEqual(tree[20], [None, None])

    def test_other_variant(self):
        """Тест с параметрами другого варианта (например, вариант 1)."""
        tree = gen_bin_tree(
            height=2,
            root=1,
            left_branch=lambda x: x * 2,
            right_branch=lambda x: x + 3,
        )

        self.assertEqual(tree[1], [2, 4])
        self.assertEqual(tree[2], [None, None])
        self.assertEqual(tree[4], [None, None])

    def test_invalid_height(self):
        """Тест с некорректным параметром высоты."""
        with self.assertRaises(ValueError):
            gen_bin_tree(height=0)

        with self.assertRaises(ValueError):
            gen_bin_tree(height=-1)

    def test_tree_structure_integrity(self):
        """Тест целостности структуры дерева."""
        tree = gen_bin_tree(height=3)

        for node, children in tree.items():
            self.assertEqual(len(children), 2)

            for child in children:
                self.assertTrue(isinstance(child, int) or child is None)

    def test_no_duplicate_nodes(self):
        """Тест отсутствия дубликатов узлов в дереве."""
        tree = gen_bin_tree(height=4)
        nodes = list(tree.keys())
        self.assertEqual(len(nodes), len(set(nodes)))


if __name__ == "__main__":
    unittest.main()