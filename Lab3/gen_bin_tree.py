from typing import Any, Callable
from pprint import pprint


def gen_bin_tree(
        height: int,
        root: int,
        l_b: Callable[[int], int] = lambda x: x * 2,
        r_b: Callable[[int], int] = lambda x: x + 3
) -> dict[str, list[Any]]:
    """Генерирует двоичное дерево заданной высоты с корнем и заданными правилами ветвления.

    Args:
        height (int): Высота дерева. Должна быть положительным целым числом.
            При height <= 1 возвращается лист.
        root (int): Значение корневого узла.
        l_b (Callable[[int], int], optional): Функция для вычисления левого потомка.
            По умолчанию: lambda x: x * 2.
        r_b (Callable[[int], int], optional): Функция для вычисления правого потомка.
            По умолчанию: lambda x: x + 3.

    Returns:
        dict[str, list[Any]]: Словарь, представляющий корень дерева.
            Ключ — строка с текущим значением узла.
            Значение — список из двух элементов: левое и правое поддеревья.
            Для листьев список пуст.
    """
    if height <= 1:
        return {str(root): []}
    return {
        str(root): [
            gen_bin_tree(height - 1, l_b(root), l_b, r_b),
            gen_bin_tree(height - 1, r_b(root), l_b, r_b)
        ]
    }


def print_bin_tree(tree: dict[str, list[Any]]) -> None:
    """Печатает двоичное дерево читаемом формате с использованием pprint.

    Args:
        tree (dict[str, list[Any]]): Дерево, представленное в виде вложенного словаря.
    """
    pprint(tree)
