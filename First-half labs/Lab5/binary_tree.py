from collections import deque
from typing import Dict, List, Optional, Callable


def gen_bin_tree(
        height: int = 5,
        root: int = 18,
        left_branch: Callable[[int], int] = lambda x: (x - 8) * 3,
        right_branch: Callable[[int], int] = lambda x: (x + 8) * 2,
) -> Dict[int, List[Optional[int]]]:
    """
    Сгенерировать бинарное дерево итеративно (без рекурсии).

    Функция строит бинарное дерево, где каждый узел имеет двух потомков.
    Потомки вычисляются с использованием предоставленных функций
    left_branch и right_branch. Дерево строится уровень за уровнем
    (поиск в ширину) до достижения указанной высоты.

    Аргументы:
        height: Высота дерева (количество уровней).
                Должна быть >= 1. По умолчанию 5.
        root: Значение корневого узла. По умолчанию 18.
        left_branch: Функция для вычисления левого потомка из родительского узла.
                     По умолчанию (родитель - 8) * 3.
        right_branch: Функция для вычисления правого потомка из родительского узла.
                      По умолчанию (родитель + 8) * 2.

    Возвращает:
        Словарь, представляющий бинарное дерево.
        Ключи - значения узлов, значения - списки [левый_потомок, правый_потомок].
        Листовые узлы имеют [None, None] в качестве потомков.
        Возвращает пустой словарь, если height < 1.

    Исключения:
        ValueError: Если высота меньше 1.

    Примеры:
        >>> tree = gen_bin_tree(height=2, root=18)
        >>> tree[18]
        [30, 52]
    """
    if height < 1:
        raise ValueError("Высота должна быть больше или равна 1")

    tree = {}
    queue = deque([(root, 1)])

    while queue:
        current_node, level = queue.popleft()

        if current_node in tree:
            continue

        if level < height:
            left_child = left_branch(current_node)
            right_child = right_branch(current_node)
            tree[current_node] = [left_child, right_child]

            queue.append((left_child, level + 1))
            queue.append((right_child, level + 1))
        else:
            tree[current_node] = [None, None]

    return tree


def print_tree(tree: Dict[int, List[Optional[int]]]) -> None:
    """
    Вывести бинарное дерево в удобочитаемом формате.

    Аргументы:
        tree: Словарь бинарного дерева для вывода.
    """
    if not tree:
        print("Дерево пустое")
        return

    print("Структура бинарного дерева:")
    print("-" * 40)

    for node, children in tree.items():
        left_str = children[0] if children[0] is not None else "None"
        right_str = children[1] if children[1] is not None else "None"
        print(f"Узел {node}: левый = {left_str}, правый = {right_str}")

    print("-" * 40)

