import os
from typing import Dict, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def create_vector() -> np.ndarray:
    """
    Создать массив от 0 до 9.

    Returns:
        np.ndarray: Массив чисел от 0 до 9 включительно.
    """
    return np.arange(10)


def create_matrix() -> np.ndarray:
    """
    Создать матрицу 5x5 со случайными числами [0, 1].

    Returns:
        np.ndarray: Матрица 5x5 со случайными значениями от 0 до 1.
    """
    return np.random.rand(5, 5)


def reshape_vector(vec: np.ndarray) -> np.ndarray:
    """
    Преобразовать форму массива из (10,) в (2, 5).

    Args:
        vec: Входной массив формы (10,).

    Returns:
        np.ndarray: Преобразованный массив формы (2, 5).
    """
    return vec.reshape(2, 5)


def transpose_matrix(mat: np.ndarray) -> np.ndarray:
    """
    Выполнить транспонирование матрицы.

    Args:
        mat: Входная матрица.

    Returns:
        np.ndarray: Транспонированная матрица.
    """
    return mat.T


def vector_add(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Сложить два вектора одинаковой длины.

    Args:
        a: Первый вектор.
        b: Второй вектор.

    Returns:
        np.ndarray: Результат поэлементного сложения.
    """
    return a + b


def scalar_multiply(vec: np.ndarray, scalar: Union[float, int]) -> np.ndarray:
    """
    Умножить вектор на число (скаляр).

    Args:
        vec: Входной вектор.
        scalar: Число для умножения.

    Returns:
        np.ndarray: Результат умножения вектора на скаляр.
    """
    return vec * scalar


def elementwise_multiply(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Выполнить поэлементное умножение массивов.

    Args:
        a: Первый массив.
        b: Второй массив.

    Returns:
        np.ndarray: Результат поэлементного умножения.
    """
    return a * b


def dot_product(a: np.ndarray, b: np.ndarray) -> float:
    """
    Вычислить скалярное произведение двух векторов.

    Args:
        a: Первый вектор.
        b: Второй вектор.

    Returns:
        float: Скалярное произведение.
    """
    return float(np.dot(a, b))


def matrix_multiply(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Выполнить матричное умножение (произведение матриц).

    Args:
        a: Первая матрица.
        b: Вторая матрица.

    Returns:
        np.ndarray: Результат умножения матриц.
    """
    return a @ b


def matrix_determinant(a: np.ndarray) -> float:
    """
    Вычислить определитель квадратной матрицы.

    Args:
        a: Квадратная матрица.

    Returns:
        float: Определитель матрицы.
    """
    return float(np.linalg.det(a))


def matrix_inverse(a: np.ndarray) -> np.ndarray:
    """
    Вычислить обратную матрицу.

    Args:
        a: Квадратная матрица.

    Returns:
        np.ndarray: Обратная матрица.
    """
    return np.linalg.inv(a)


def solve_linear_system(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Решить систему линейных уравнений вида Ax = b.

    Args:
        a: Матрица коэффициентов A.
        b: Вектор свободных членов b.

    Returns:
        np.ndarray: Решение системы x.
    """
    return np.linalg.solve(a, b)


def load_dataset(path: str = "data/students_scores.csv") -> np.ndarray:
    """
    Загрузить данные из CSV-файла и преобразовать их в NumPy массив.

    Args:
        path: Путь к CSV файлу.

    Returns:
        np.ndarray: Данные в виде массива.
    """
    return pd.read_csv(path).to_numpy()


def statistical_analysis(data: np.ndarray) -> Dict[str, float]:
    """
    Провести статистический анализ одномерного массива данных.

    Args:
        data: Одномерный массив данных.

    Returns:
        Dict[str, float]: Словарь с показателями (mean, median, std, min, max, q1, q3).
    """
    return {
        "mean": float(np.mean(data)),
        "median": float(np.median(data)),
        "std": float(np.std(data)),
        "min": float(np.min(data)),
        "max": float(np.max(data)),
        "q1": float(np.percentile(data, 25)),
        "q3": float(np.percentile(data, 75))
    }


def normalize_data(data: np.ndarray) -> np.ndarray:
    """
    Выполнить Min-Max нормализацию данных.

    Формула: (x - min) / (max - min)

    Args:
        data: Входной массив данных.

    Returns:
        np.ndarray: Нормализованный массив в диапазоне [0, 1].
    """
    data_min = np.min(data)
    data_max = np.max(data)
    return (data - data_min) / (data_max - data_min)


def plot_histogram(data: np.ndarray) -> None:
    """
    Построить и сохранить гистограмму распределения данных.

    Args:
        data: Данные для визуализации.
    """
    os.makedirs("plots", exist_ok=True)
    plt.figure()
    plt.hist(data, bins=5, color='skyblue', edgecolor='black')
    plt.title("Распределение оценок")
    plt.xlabel("Баллы")
    plt.ylabel("Количество студентов")
    plt.savefig("plots/histogram.png")
    plt.close()


def plot_heatmap(matrix: np.ndarray) -> None:
    """
    Построить и сохранить тепловую карту корреляции.

    Args:
        matrix: Квадратная матрица для визуализации.
    """
    os.makedirs("plots", exist_ok=True)
    plt.figure(figsize=(8, 6))
    sns.heatmap(matrix, annot=True, cmap='magma')
    plt.title("Тепловая карта корреляции")
    plt.savefig("plots/heatmap.png")
    plt.close()


def plot_line(x: np.ndarray, y: np.ndarray) -> None:
    """
    Построить и сохранить линейный график зависимости.

    Args:
        x: Данные для оси X (например, ID студентов).
        y: Данные для оси Y (например, оценки).
    """
    os.makedirs("plots", exist_ok=True)
    plt.figure()
    plt.plot(x, y, marker='o', linestyle='-', color='green')
    plt.title("Оценки по математике")
    plt.xlabel("ID студента")
    plt.ylabel("Оценка")
    plt.grid(True)
    plt.savefig("plots/line_plot.png")
    plt.close()