from main import *


def test_create_vector() -> None:
    """Проверить создание вектора от 0 до 9."""
    v = create_vector()
    assert isinstance(v, np.ndarray)
    assert v.shape == (10,)
    assert np.array_equal(v, np.arange(10))


def test_create_matrix() -> None:
    """Проверить создание матрицы 5x5 со случайными значениями."""
    m = create_matrix()
    assert isinstance(m, np.ndarray)
    assert m.shape == (5, 5)
    assert np.all((m >= 0) & (m < 1))


def test_reshape_vector() -> None:
    """Проверить изменение формы вектора (10,) -> (2, 5)."""
    v = np.arange(10)
    reshaped = reshape_vector(v)
    assert reshaped.shape == (2, 5)
    assert reshaped[0, 0] == 0
    assert reshaped[1, 4] == 9


def test_transpose_matrix() -> None:
    """Проверить транспонирование матрицы."""
    m = np.array([[1, 2], [3, 4]])
    expected = np.array([[1, 3], [2, 4]])
    assert np.array_equal(transpose_matrix(m), expected)


def test_vector_add() -> None:
    """Проверить поэлементное сложение векторов."""
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    assert np.array_equal(vector_add(a, b), np.array([5, 7, 9]))


def test_scalar_multiply() -> None:
    """Проверить умножение вектора на скаляр."""
    v = np.array([1, 2, 3])
    assert np.array_equal(scalar_multiply(v, 2), np.array([2, 4, 6]))


def test_elementwise_multiply() -> None:
    """Проверить поэлементное умножение массивов."""
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    assert np.array_equal(elementwise_multiply(a, b), np.array([4, 10, 18]))


def test_dot_product() -> None:
    """Проверить скалярное произведение векторов."""
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    assert dot_product(a, b) == 32


def test_matrix_multiply() -> None:
    """Проверить матричное умножение."""
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[2, 0], [1, 2]])
    assert np.array_equal(matrix_multiply(a, b), a @ b)


def test_matrix_determinant() -> None:
    """Проверить вычисление определителя матрицы."""
    a = np.array([[1, 2], [3, 4]])
    assert round(matrix_determinant(a), 5) == -2.0


def test_matrix_inverse() -> None:
    """Проверить нахождение обратной матрицы."""
    a = np.array([[1, 2], [3, 4]])
    inv_a = matrix_inverse(a)
    assert np.allclose(a @ inv_a, np.eye(2))


def test_solve_linear_system() -> None:
    """Проверить решение системы линейных уравнений Ax = b."""
    a = np.array([[2, 1], [1, 3]])
    b = np.array([1, 2])
    x = solve_linear_system(a, b)
    assert np.allclose(a @ x, b)


def test_load_dataset() -> None:
    """Проверить загрузку данных из CSV файла."""
    test_file = "test_data.csv"
    test_content = "math,physics,informatics\n78,81,90\n85,89,88"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(test_content)
    try:
        data = load_dataset(test_file)
        assert data.shape == (2, 3)
        assert np.array_equal(data[0], [78, 81, 90])
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)


def test_statistical_analysis() -> None:
    """Проверить корректность статистических вычислений."""
    data = np.array([10, 20, 30])
    result = statistical_analysis(data)
    assert result["mean"] == 20
    assert result["min"] == 10
    assert result["max"] == 30


def test_normalization() -> None:
    """Проверить Min-Max нормализацию массива."""
    data = np.array([0, 5, 10])
    norm = normalize_data(data)
    assert np.allclose(norm, np.array([0, 0.5, 1]))


def test_plot_histogram() -> None:
    """Проверить запуск функции построения гистограммы."""
    data = np.array([1, 2, 3, 4, 5])
    plot_histogram(data)
    assert os.path.exists("plots/histogram.png")


def test_plot_heatmap() -> None:
    """Проверить запуск функции построения тепловой карты."""
    matrix = np.array([[1, 0.5], [0.5, 1]])
    plot_heatmap(matrix)
    assert os.path.exists("plots/heatmap.png")


def test_plot_line() -> None:
    """Проверить запуск функции построения линейного графика."""
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    plot_line(x, y)
    assert os.path.exists("plots/line_plot.png")