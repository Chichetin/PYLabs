# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False

import math
from libc.math cimport cos as c_cos

# cpdef делает функцию доступной и из Python, и из C
cpdef double integrate_cython(double a, double b, int n_iter=1000000):
    """
    Оптимизированная версия на Cython.
    Использует статическую типизацию и C-функцию cos.
    """
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i

    for i in range(n_iter):
        # Используем c_cos (функция из стандартной библиотеки C),
        # чтобы не вызывать медленный math.cos из Python
        acc += c_cos(a + i * step) * step

    return acc

# Итерация 5: Версия с отпусканием GIL
def integrate_nogil(double a, double b, int n_iter=1000000):
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i

    # Блок nogil позволяет потокам выполнять этот цикл параллельно в настоящем смысле
    with nogil:
        for i in range(n_iter):
            acc += c_cos(a + i * step) * step

    return acc