import math
from typing import Dict, List, Any, Optional
from .naibbe.encoder import NaibbeEncoder
from .naibbe.signatures import compute_sig1, compute_sig2, compute_sig3, compute_sig4

def calculate_percentile(sorted_list: List[float], val: float) -> float:
    """Calculates empirical percentile of val in sorted_list."""
    if not sorted_list:
        return 0.0
    count = sum(1 for x in sorted_list if x <= val)
    return (count / len(sorted_list)) * 100.0

def calculate_stats(values: List[float], observed_val: float) -> Dict[str, Any]:
    """
    Computes statistical comparison metrics (mean, std, z-score, confidence 
    intervals, percentile rank) for an observed value against a simulated 
    null distribution.
    
    Args:
        values: List of simulated values.
        observed_val: The observed value from the Voynich manuscript.
        
    Returns:
        Dictionary containing comparative statistics.
    """
    if not values:
        return {}
    n = len(values)
    mean = sum(values) / n
    variance = sum((x - mean)**2 for x in values) / (n - 1) if n > 1 else 0.0
    std_dev = math.sqrt(variance)
    
    sorted_vals = sorted(values)
    idx_2_5 = max(0, int(n * 0.025))
    idx_97_5 = min(n - 1, int(n * 0.975))
    ci_lower = sorted_vals[idx_2_5]
    ci_upper = sorted_vals[idx_97_5]
    
    z_score = (observed_val - mean) / std_dev if std_dev > 0 else 0.0
    percentile = calculate_percentile(sorted_vals, observed_val)
    outside_ci = observed_val < ci_lower or observed_val > ci_upper
    
    return {
        "mean": mean,
        "std_dev": std_dev,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "z_score": z_score,
        "percentile": percentile,
        "outside_ci": outside_ci
    }

class MonteCarloSimulator:
    """
    A simulator that orchestrates running multiple encoding runs with different
    random seeds, comparing the results against observed Voynich manuscript 
    signatures.
    """
    
    def __init__(self, observed_words: List[str]):
        """
        Initialize the simulator with observed Voynich words.
        
        Args:
            observed_words: List of words from the Voynich manuscript.
        """
        self.observed_words = observed_words
        self.observed_sigs = self._compute_dataset_signatures(observed_words)
        
    def _compute_dataset_signatures(self, words: List[str]) -> Dict[str, float]:
        """Helper to compute signatures for a dataset."""
        s1 = compute_sig1(words)
        s2 = compute_sig2(words)
        s3 = compute_sig3(words)
        s4 = compute_sig4(words)
        
        return {
            "sig1": s1,
            "sig2_present": 1.0 if s2["present"] else 0.0,
            "sig2_starts": float(len(s2["extreme_start"])),
            "sig2_ends": float(len(s2["extreme_end"])),
            "sig3": s3,
            "sig4_start_r2": s4["start_r2"],
            "sig4_start_cv": s4["start_cv"],
            "sig4_end_r2": s4["end_r2"],
            "sig4_end_cv": s4["end_cv"]
        }
        
    def run_simulation(
        self, 
        plaintext: str, 
        num_seeds: int = 100,
        unambiguous: bool = True
    ) -> Dict[str, Dict[str, Any]]:
        """
        Runs the Monte Carlo simulation.
        Encodes the plaintext document with different seeds, computes signatures 
        for each ciphertext, and compares them to the observed Voynich signatures.
        
        Args:
            plaintext: Plaintext corpus (e.g. Pliny or Moby Dick).
            num_seeds: Number of seeds to simulate.
            unambiguous: Whether to use unambiguous encoding.
            
        Returns:
            A dictionary containing the stats for each signature.
        """
        metrics = list(self.observed_sigs.keys())
        sim_results = {m: [] for m in metrics}
        
        for seed in range(1, num_seeds + 1):
            encoder = NaibbeEncoder(seed=seed)
            ciphertext = encoder.encode(plaintext, unambiguous=unambiguous)
            words = ciphertext.split()
            
            sigs = self._compute_dataset_signatures(words)
            for m in metrics:
                sim_results[m].append(sigs[m])
                
        # Calculate comparison stats
        stats = {}
        for m in metrics:
            stats[m] = calculate_stats(sim_results[m], self.observed_sigs[m])
            stats[m]["observed"] = self.observed_sigs[m]
            
        return stats
