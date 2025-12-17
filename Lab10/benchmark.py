import timeit
import math
import pandas as pd # Для красивого вывода таблицы
from src.integrator import integrate
from src.parallel import integrate_async
# Импортируем скомпилированные функции (убедись, что выполнил setup.py)
from src.fast_logic import integrate_cython, integrate_nogil

def run_benchmarks():
    n_iterations = 10**7
    n_jobs_list = [2, 4, 6]
    results = []

    # 1. Pure Python (Baseline)
    print("Замер: Pure Python...")
    t_base = timeit.timeit(lambda: integrate(math.cos, 0, math.pi, n_iter=n_iterations), number=1)
    results.append({"Method": "Pure Python", "n_jobs": 1, "Time": t_base})

    # 2. Cython (Single Thread)
    print("Замер: Cython (Single)...")
    t_cython = timeit.timeit(lambda: integrate_cython(0, math.pi, n_iter=n_iterations), number=1)
    results.append({"Method": "Cython", "n_jobs": 1, "Time": t_cython})

    # 3. Parallel Benchmarks
    for n in n_jobs_list:
        print(f"Замер: Threads/Processes с n_jobs={n}...")

        # Threads (Pure Python)
        t_th = timeit.timeit(lambda: integrate_async(math.cos, 0, math.pi, n_jobs=n, n_iter=n_iterations, executor_type='threads'), number=1)
        results.append({"Method": "Threads (Python)", "n_jobs": n, "Time": t_th})

        # Processes (Pure Python)
        t_pr = timeit.timeit(lambda: integrate_async(math.cos, 0, math.pi, n_jobs=n, n_iter=n_iterations, executor_type='processes'), number=1)
        results.append({"Method": "Processes (Python)", "n_jobs": n, "Time": t_pr})

        # Cython + noGIL + Threads (Самый быстрый вариант)
        # Здесь мы вручную вызываем пул для nogil функции
        import concurrent.futures as ftres
        def run_nogil_parallel():
            step = math.pi / n
            with ftres.ThreadPoolExecutor(max_workers=n) as ex:
                fs = [ex.submit(integrate_nogil, i*step, (i+1)*step, n_iterations//n) for i in range(n)]
                return sum(f.result() for f in ftres.as_completed(fs))

        t_nogil = timeit.timeit(run_nogil_parallel, number=1)
        results.append({"Method": "Cython + noGIL (Threads)", "n_jobs": n, "Time": t_nogil})

    # Вывод результатов
    df = pd.DataFrame(results)

    print("\nИтоговая таблица производительности:")
    print(df.pivot(index='n_jobs', columns='Method', values='Time'))

if __name__ == "__main__":
    run_benchmarks()