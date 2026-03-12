import timeit
import matplotlib.pyplot as plt
from typing import Optional, List

class Node:
    """
    Класс, представляющий узел бинарного дерева.

    Attributes:
        value (int): Значение, хранящееся в узле.
        left (Optional[Node]): Левый потомок.
        right (Optional[Node]): Правый потомок.
    """
    def __init__(self, value: int):
        self.value = value
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None

def get_left_val(val: int) -> int:
    """Вычисляет значение левого потомка"""
    return (val - 8) * 3

def get_right_val(val: int) -> int:
    """Вычисляет значение правого потомка"""
    return (val + 8) * 2

def build_tree_recursive(value: int, height: int) -> Optional[Node]:
    """
    Рекурсивно строит бинарное дерево заданной высоты.

    Args:
        value (int): Значение текущего корня.
        height (int): Оставшаяся высота построения.

    Returns:
        Optional[Node]: Корень построенного поддерева или None.
    """
    if height < 0:
        return None

    node = Node(value)
    if height > 0:
        node.left = build_tree_recursive(get_left_val(value), height - 1)
        node.right = build_tree_recursive(get_right_val(value), height - 1)
    return node

def build_tree_iterative(root_value: int, max_height: int) -> Optional[Node]:
    """
    Итеративно строит бинарное дерево, используя очередь.

    Args:
        root_value (int): Значение корневого узла.
        max_height (int): Максимальная высота дерева.

    Returns:
        Optional[Node]: Корень построенного дерева.
    """
    if max_height < 0:
        return None

    root = Node(root_value)
    # Очередь хранит кортеж: (текущий_узел, текущая_глубина)
    queue: List = [(root, 0)]

    while queue:
        current_node, current_height = queue.pop(0)

        if current_height < max_height:
            # Создаем левого потомка
            current_node.left = Node(get_left_val(current_node.value))
            queue.append((current_node.left, current_height + 1))

            # Создаем правого потомка
            current_node.right = Node(get_right_val(current_node.value))
            queue.append((current_node.right, current_height + 1))

    return root

def benchmark():
    """
    Проводит замеры времени работы функций и строит график.
    """
    root_val = 18
    heights = list(range(1, 15))  # Тестируем высоту от 1 до 14
    rec_times = []
    iter_times = []

    for h in heights:
        # Замер рекурсии
        t_rec = timeit.timeit(lambda: build_tree_recursive(root_val, h), number=100)
        rec_times.append(t_rec / 100)

        # Замер итерации
        t_iter = timeit.timeit(lambda: build_tree_iterative(root_val, h), number=100)
        iter_times.append(t_iter / 100)

    # Построение графика
    plt.figure(figsize=(10, 6))
    plt.plot(heights, rec_times, label='Recursive', marker='o')
    plt.plot(heights, iter_times, label='Iterative', marker='s')
    plt.xlabel('Высота дерева (Height)')
    plt.ylabel('Среднее время выполнения (секунды)')
    plt.title('Сравнение времени построения дерева')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    benchmark()