import concurrent.futures as ftres
from functools import partial
from typing import Callable, Type, Union
from src.integrator import integrate

def integrate_async(
        f: Callable[[float], float],
        a: float,
        b: float,
        *,
        n_jobs: int = 2,
        n_iter: int = 1000000,
        executor_type: str = 'threads'
) -> float:
    """
    Параллельная реализация интегрирования.

    Args:
        f: Интегрируемая функция.
        a, b: Границы интервала.
        n_jobs: Количество воркеров (потоков или процессов).
        n_iter: Общее количество итераций (делится между воркерами).
        executor_type: Тип параллелизма ('threads' или 'processes').
    """

    # Выбор исполнителя
    if executor_type == 'threads':
        executor_class: Type[ftres.Executor] = ftres.ThreadPoolExecutor
    elif executor_type == 'processes':
        executor_class = ftres.ProcessPoolExecutor
    else:
        raise ValueError("executor_type must be 'threads' or 'processes'")

    # Рассчитываем параметры для каждого воркера
    step_size = (b - a) / n_jobs
    iters_per_job = n_iter // n_jobs

    with executor_class(max_workers=n_jobs) as executor:
        # partial фиксирует функцию и количество итераций для передачи в executor
        spawn = partial(executor.submit, integrate, f, n_iter=iters_per_job)

        futures = []
        for i in range(n_jobs):
            # Рассчитываем локальные границы для каждого воркера
            start = a + i * step_size
            end = a + (i + 1) * step_size
            futures.append(spawn(start, end))

        # Собираем результаты по мере готовности и суммируем
        return sum(future.result() for future in ftres.as_completed(futures))

if __name__ == "__main__":
    import math
    import time

    # Пример замера производительности
    print("Сравнение производительности (n_iter=10^7):")
    for mode in ['threads', 'processes']:
        start_time = time.time()
        res = integrate_async(math.sin, 0, math.pi, n_jobs=4, n_iter=10**7, executor_type=mode)
        duration = time.time() - start_time
        print(f"Режим {mode:10}: {duration:.4f} сек. Результат: {res:.6f}")