import math
import unittest

from src.vendor_performance.metrics import confidence_interval, format_currency, herfindahl_hirschman_index


class MetricsTests(unittest.TestCase):
    def test_format_currency(self) -> None:
        self.assertEqual(format_currency(1_250_000), "$1.25M")
        self.assertEqual(format_currency(950), "$950.00")

    def test_confidence_interval_single_value(self) -> None:
        mean_value, lower_bound, upper_bound = confidence_interval([42.0])
        self.assertEqual(mean_value, 42.0)
        self.assertEqual(lower_bound, 42.0)
        self.assertEqual(upper_bound, 42.0)

    def test_hhi(self) -> None:
        hhi = herfindahl_hirschman_index([50, 30, 20])
        self.assertTrue(math.isclose(hhi, 0.38, rel_tol=1e-2))


if __name__ == "__main__":
    unittest.main()
