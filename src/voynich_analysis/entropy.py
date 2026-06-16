import math
import random
from collections import Counter
from typing import Dict, List, Tuple, Union, Optional

def compute_h1(chars: Union[str, List[str]]) -> float:
    """
    Computes first-order Shannon entropy (H1) for a sequence of characters.
    
    H1 = -sum(p(x) * log2(p(x)))
    
    Args:
        chars: A string or list of characters.
        
    Returns:
        The first-order entropy in bits.
    """
    n = len(chars)
    if n == 0:
        return 0.0
    counts = Counter(chars)
    return -sum((c / n) * math.log2(c / n) for c in counts.values() if c > 0)

def compute_h2(chars: Union[str, List[str]]) -> float:
    """
    Computes second-order Shannon entropy (H2) for a sequence of characters
    using bigrams.
    
    H2 = -sum(p(x, y) * log2(p(x, y)))
    
    Args:
        chars: A string or list of characters.
        
    Returns:
        The second-order entropy in bits.
    """
    n = len(chars) - 1
    if n <= 0:
        return 0.0
    # Create character bigrams
    bigrams = [chars[i] + chars[i+1] for i in range(n)]
    counts = Counter(bigrams)
    return -sum((c / n) * math.log2(c / n) for c in counts.values() if c > 0)

def compute_metrics(chars: Union[str, List[str]]) -> Dict[str, Union[float, int]]:
    """
    Computes H1, H2, conditional entropy (Hcond), and the R-ratio (H2/H1^2).
    
    Args:
        chars: A string or list of characters.
        
    Returns:
        A dictionary containing H1, H2, Hcond, R, and N (sample size).
    """
    h1 = compute_h1(chars)
    h2 = compute_h2(chars)
    hcond = h2 - h1
    r = h2 / (h1 ** 2) if h1 > 0 else 0.0
    return {
        "H1": h1,
        "H2": h2,
        "Hcond": hcond,
        "R": r,
        "N": len(chars)
    }

def shuffle_null_distribution(
    chars: Union[str, List[str]], 
    n_shuffles: int = 500, 
    seed: Optional[int] = None
) -> Tuple[float, float, List[float]]:
    """
    Estimates the null distribution of the R-ratio (H2/H1^2) by repeatedly 
    shuffling the character sequence. This breaks bigram structure while
    preserving unigram frequency.
    
    Args:
        chars: A string or list of characters.
        n_shuffles: Number of shuffles to execute.
        seed: Random seed for reproducibility.
        
    Returns:
        A tuple of (mean_R, std_dev_R, all_shuffled_R_values).
    """
    if seed is not None:
        random.seed(seed)
        
    r_values = []
    chars_list = list(chars)
    for _ in range(n_shuffles):
        random.shuffle(chars_list)
        m = compute_metrics(chars_list)
        r_values.append(m["R"])
        
    mean_r = sum(r_values) / len(r_values)
    variance = sum((x - mean_r)**2 for x in r_values) / (len(r_values) - 1) if len(r_values) > 1 else 0.0
    std_r = math.sqrt(variance)
    return mean_r, std_r, r_values

def analyze_entropy_significance(
    chars: Union[str, List[str]], 
    n_shuffles: int = 500, 
    seed: Optional[int] = None
) -> Dict[str, Any]:
    """
    Runs full Shannon entropy analysis on a character sequence, comparing the
    observed metrics to a shuffle-null distribution.
    
    Args:
        chars: A string or list of characters.
        n_shuffles: Number of shuffle runs.
        seed: Random seed.
        
    Returns:
        A dictionary with observed metrics, null stats, net R, and z-score.
    """
    # Import locally to avoid potential circular dependencies
    global Any
    from typing import Any
    
    obs = compute_metrics(chars)
    mean_null, std_null, null_vals = shuffle_null_distribution(chars, n_shuffles, seed)
    
    z_score = (obs["R"] - mean_null) / std_null if std_null > 0 else 0.0
    net_r = obs["R"] - mean_null
    
    # Calculate percentile rank of observed R in null values
    sorted_null = sorted(null_vals)
    count = sum(1 for x in sorted_null if x <= obs["R"])
    percentile = (count / len(sorted_null)) * 100.0 if sorted_null else 0.0
    
    return {
        "N": obs["N"],
        "H1": obs["H1"],
        "H2": obs["H2"],
        "Hcond": obs["Hcond"],
        "R_observed": obs["R"],
        "R_null_mean": mean_null,
        "R_null_std": std_null,
        "Net_R": net_r,
        "z_score": z_score,
        "percentile": percentile
    }
