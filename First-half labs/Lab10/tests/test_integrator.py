import unittest
import math
from src.integrator import integrate

class TestIntegrator(unittest.TestCase):
    def test_trigonometric(self):
        """Проверка точности для тригонометрической функции sin(x) на [0, pi]."""
        # Интеграл sin(x) от 0 до pi равен 2.0
        result = integrate(math.sin, 0, math.pi, n_iter=10**6)
        self.assertAlmostEqual(result, 2.0, places=5)

    def test_polynomial(self):
        """Проверка точности для полинома x^2 + 2x + 1 на [0, 1]."""
        # Интеграл (x^2 + 2x + 1) dx от 0 до 1 равен 1/3 + 1 + 1 = 2.33333...
        f = lambda x: x**2 + 2*x + 1
        result = integrate(f, 0, 1, n_iter=10**6)
        self.assertAlmostEqual(result, 7/3, places=5)

    def test_iteration_stability(self):
        """Проверка устойчивости: с ростом итераций точность должна расти."""
        f = math.exp
        a, b = 0, 1
        true_value = math.e - 1

        res_low = integrate(f, a, b, n_iter=100)
        res_high = integrate(f, a, b, n_iter=10000)

        # Погрешность при большем числе итераций должна быть меньше
        self.assertLess(abs(res_high - true_value), abs(res_low - true_value))

if __name__ == "__main__":
    unittest.main()