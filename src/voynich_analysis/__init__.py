"""
Voynich Statistical Analysis Toolkit
====================================

A clean, modular Python toolkit for computational and statistical analysis of 
the Voynich Manuscript, utilizing Shannon entropy, Monte Carlo simulations,
and Naibbe-replication/Parisel-signature analysis.
"""

from .entropy import (
    compute_h1,
    compute_h2,
    compute_metrics,
    shuffle_null_distribution,
    analyze_entropy_significance
)
from .monte_carlo import MonteCarloSimulator

__version__ = "0.1.0"
__all__ = [
    "compute_h1",
    "compute_h2",
    "compute_metrics",
    "shuffle_null_distribution",
    "analyze_entropy_significance",
    "MonteCarloSimulator",
]
