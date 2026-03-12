from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize(
        "src/fast_logic.pyx",
        annotate=True  # Создаст HTML-файл, где желтым цветом подсвечены медленные места
    )
)