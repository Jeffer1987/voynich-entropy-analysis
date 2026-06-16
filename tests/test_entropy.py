import unittest
from voynich_analysis.entropy import compute_h1, compute_h2, compute_metrics, shuffle_null_distribution

class TestEntropy(unittest.TestCase):
    def test_compute_h1_empty(self):
        self.assertEqual(compute_h1(""), 0.0)
        self.assertEqual(compute_h1([]), 0.0)

    def test_compute_h1_uniform(self):
        # 4 distinct items should give log2(4) = 2 bits
        self.assertEqual(compute_h1("abcd"), 2.0)
        # Single item should give 0.0 bits
        self.assertEqual(compute_h1("aaaa"), 0.0)

    def test_compute_h2_empty(self):
        self.assertEqual(compute_h2(""), 0.0)
        self.assertEqual(compute_h2(["a"]), 0.0)

    def test_compute_h2_uniform(self):
        # 'aba' has bigrams 'ab', 'ba' (uniform)
        # H2 should be log2(2) = 1.0 bit
        self.assertEqual(compute_h2("aba"), 1.0)

    def test_compute_metrics(self):
        metrics = compute_metrics("abcd")
        self.assertIn("H1", metrics)
        self.assertIn("H2", metrics)
        self.assertIn("Hcond", metrics)
        self.assertIn("R", metrics)
        self.assertEqual(metrics["N"], 4)

    def test_shuffle_null_distribution(self):
        mean_r, std_r, vals = shuffle_null_distribution("abcdefghij", n_shuffles=10, seed=42)
        self.assertEqual(len(vals), 10)
        self.assertGreater(mean_r, 0)
        self.assertTrue(isinstance(std_r, float))

if __name__ == '__main__':
    unittest.main()
