#!/usr/bin/env python
"""
Example Script: Voynich Manuscript Computational and Statistical Analysis

This script demonstrates:
1. Shannon entropy analysis with shuffle-null significance tests on the Voynich text.
2. Encoding reference text (e.g. Pliny) using the Naibbe Encoder.
3. Positional signature analysis (Parisel signatures).
4. Running a mini Monte Carlo simulation comparing Naibbe-encoded texts to the Voynich.
"""

import os
import sys

# Add src to python path if run directly from repository
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from voynich_analysis.entropy import analyze_entropy_significance
from voynich_analysis.naibbe.encoder import NaibbeEncoder
from voynich_analysis.naibbe.signatures import (
    compute_sig1,
    compute_sig2,
    compute_sig3,
    compute_sig4
)
from voynich_analysis.monte_carlo import MonteCarloSimulator

def main():
    # Setup paths relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(script_dir, "..", ".."))
    
    voynich_path = os.path.join(parent_dir, "voynich.txt")
    pliny_path = os.path.join(parent_dir, "pliny.txt")
    moby_path = os.path.join(parent_dir, "mobydick.txt")
    
    # Check if files exist
    files_exist = True
    for p in [voynich_path, pliny_path, moby_path]:
        if not os.path.exists(p):
            print(f"Warning: Dataset file not found at: {p}")
            files_exist = False
            
    if not files_exist:
        print("Note: Run this example from within the git repository workspace so it can locate raw data files.")
        return

    print("=" * 80)
    print("  VOYNICH MANUSCRIPT PORTFOLIO PROJECT DEMO")
    print("=" * 80)

    # 1. Entropy analysis
    print("\n[1] Running Shannon Entropy Analysis on Voynich Manuscript...")
    with open(voynich_path, "r", encoding="utf-8") as f:
        voy_text = f.read().strip()
    
    voy_chars = [c.lower() for c in voy_text if c.isalpha()]
    entropy_results = analyze_entropy_significance(voy_chars, n_shuffles=100, seed=42)
    
    print(f"  Character count (N)    : {entropy_results['N']}")
    print(f"  H1 (Unigram Entropy)   : {entropy_results['H1']:.4f} bits")
    print(f"  H2 (Bigram Entropy)    : {entropy_results['H2']:.4f} bits")
    print(f"  R-Ratio (H2 / H1^2)    : {entropy_results['R_observed']:.4f}")
    print(f"  Shuffle-null R Mean    : {entropy_results['R_null_mean']:.4f}")
    print(f"  Net R (R_obs - R_null) : {entropy_results['Net_R']:.4f}")
    print(f"  Z-Score                : {entropy_results['z_score']:.2f}")

    # 2. Naibbe Encoder
    print("\n[2] Encoding Pliny the Elder Plaintext with NaibbeEncoder...")
    with open(pliny_path, "r", encoding="utf-8") as f:
        pliny_text = f.read().strip()
        
    encoder = NaibbeEncoder(seed=42)
    pliny_cipher = encoder.encode(pliny_text, unambiguous=True)
    
    print("  Plaintext Sample :", pliny_text[:50].replace('\n', ' '))
    print("  Ciphertext Sample:", pliny_cipher[:80], "...")

    # 3. Positional Signatures
    print("\n[3] Computing Parisel Positional Signatures...")
    voy_words = voy_text.split()
    pliny_cipher_words = pliny_cipher.split()
    
    v_s1 = compute_sig1(voy_words)
    v_s2 = compute_sig2(voy_words)
    v_s3 = compute_sig3(voy_words)
    v_s4 = compute_sig4(voy_words)
    
    p_s1 = compute_sig1(pliny_cipher_words)
    p_s2 = compute_sig2(pliny_cipher_words)
    p_s3 = compute_sig3(pliny_cipher_words)
    p_s4 = compute_sig4(pliny_cipher_words)
    
    print(f"  {'Metric':<25} | {'Voynich':<15} | {'Pliny Cipher':<15}")
    print("-" * 65)
    print(f"  {'Sig1 (E->S Ratio)':<25} | {v_s1*100:13.1f}% | {p_s1*100:13.1f}%")
    print(f"  {'Sig2 Bilateral Present':<25} | {str(v_s2['present']):<15} | {str(p_s2['present']):<15}")
    print(f"  {'Sig3 Mutual Info (bits)':<25} | {v_s3:14.4f} | {p_s3:14.4f}")
    print(f"  {'Sig4 Start R^2':<25} | {v_s4['start_r2']:14.4f} | {p_s4['start_r2']:14.4f}")
    
    # 4. Monte Carlo Simulator
    print("\n[4] Running Quick Monte Carlo Simulation (N=10 seeds)...")
    simulator = MonteCarloSimulator(voy_words)
    stats = simulator.run_simulation(pliny_text, num_seeds=10, unambiguous=True)
    
    print(f"  {'Metric':<20} | {'Observed':<10} | {'Sim Mean':<10} | {'Sim Std':<10} | {'Z-Score':<10}")
    print("-" * 70)
    for m in ["sig1", "sig3", "sig4_start_r2", "sig4_end_r2"]:
        m_stats = stats[m]
        print(f"  {m:<20} | {m_stats['observed']:<10.4f} | {m_stats['mean']:<10.4f} | {m_stats['std_dev']:<10.4f} | {m_stats['z_score']:<10.2f}")
        
    print("\n" + "=" * 80)
    print("  Demo Complete.")
    print("=" * 80)

if __name__ == "__main__":
    main()
