import unittest
from voynich_analysis.monte_carlo import calculate_stats, MonteCarloSimulator

class TestMonteCarlo(unittest.TestCase):
    def test_calculate_stats(self):
        simulated_values = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
        stats = calculate_stats(simulated_values, 1.5)
        
        self.assertEqual(stats["mean"], 1.5)
        self.assertEqual(stats["z_score"], 0.0)
        self.assertFalse(stats["outside_ci"])
        self.assertTrue(0.0 <= stats["percentile"] <= 100.0)

    def test_monte_carlo_simulator(self):
        observed_voynich_words = ["<ol>", "<chedy>", "<daiin>", "<shedy>", "<qokaiin>"]
        simulator = MonteCarloSimulator(observed_voynich_words)
        
        plaintext_ref = "This is a simple reference text to run a quick test simulation with."
        stats = simulator.run_simulation(plaintext_ref, num_seeds=3, unambiguous=True)
        
        self.assertIn("sig1", stats)
        self.assertIn("sig3", stats)
        self.assertIn("observed", stats["sig1"])
        self.assertIn("mean", stats["sig1"])

if __name__ == '__main__':
    unittest.main()
