import argparse
import sys
import os
from .entropy import analyze_entropy_significance
from .naibbe.encoder import NaibbeEncoder
from .monte_carlo import MonteCarloSimulator

def main() -> None:
    """
    Main command-line interface entry point.
    """
    parser = argparse.ArgumentParser(
        description="Voynich Manuscript Statistical Analysis and Simulation Toolkit"
    )
    subparsers = parser.add_subparsers(dest="command", help="Analysis commands")
    
    # Entropy command
    entropy_parser = subparsers.add_parser("entropy", help="Shannon Entropy and shuffle null analysis")
    entropy_parser.add_argument("file", help="Path to text file to analyze")
    entropy_parser.add_argument("--shuffles", type=int, default=500, help="Number of shuffles for null distribution")
    entropy_parser.add_argument("--seed", type=int, default=42, help="Random seed for shuffles")
    
    # Simulate command
    sim_parser = subparsers.add_parser("simulate", help="Run Naibbe encoder Monte Carlo simulation")
    sim_parser.add_argument("--voynich", required=True, help="Path to observed Voynich text file")
    sim_parser.add_argument("--reference", required=True, help="Path to reference plaintext file (e.g. Pliny, Moby Dick)")
    sim_parser.add_argument("--seeds", type=int, default=100, help="Number of simulation seeds to run")
    sim_parser.add_argument("--ambiguous", action="store_true", default=False, help="Allow ambiguous bigram/unigram clashing")
    
    args = parser.parse_args()
    
    if args.command == "entropy":
        run_entropy(args)
    elif args.command == "simulate":
        run_simulate(args)
    else:
        parser.print_help()
        sys.exit(1)

def run_entropy(args: argparse.Namespace) -> None:
    if not os.path.exists(args.file):
        print(f"Error: File not found: {args.file}")
        sys.exit(1)
        
    print(f"Reading file: {args.file}...")
    with open(args.file, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read().strip()
        
    chars = [c.lower() for c in text if c.isalpha()]
    print(f"Character count (alphabetic): {len(chars)}")
    
    if len(chars) < 100:
        print("Error: Input file has insufficient alphabetic data (need at least 100 characters).")
        sys.exit(1)
        
    print(f"Running entropy analysis with {args.shuffles} shuffles...")
    res = analyze_entropy_significance(chars, n_shuffles=args.shuffles, seed=args.seed)
    
    print("\n" + "=" * 50)
    print("         SHANNON ENTROPY ANALYSIS RESULTS")
    print("=" * 50)
    print(f"Sample Size (N)       : {res['N']}")
    print(f"H1 (Unigram Entropy)  : {res['H1']:.6f} bits")
    print(f"H2 (Bigram Entropy)   : {res['H2']:.6f} bits")
    print(f"Hcond (Conditional)   : {res['Hcond']:.6f} bits")
    print(f"R-Ratio (H2 / H1^2)   : {res['R_observed']:.6f}")
    print("-" * 50)
    print("SHUFFLE-NULL DISTRIBUTIONS:")
    print(f"Null R-Ratio Mean     : {res['R_null_mean']:.6f}")
    print(f"Null R-Ratio StdDev   : {res['R_null_std']:.6f}")
    print(f"Net R (Obs - Null)    : {res['Net_R']:.6f}")
    print(f"Z-Score               : {res['z_score']:.2f}")
    print(f"Empirical Percentile  : {res['percentile']:.1f}%")
    print("=" * 50)

def run_simulate(args: argparse.Namespace) -> None:
    if not os.path.exists(args.voynich):
        print(f"Error: Voynich file not found: {args.voynich}")
        sys.exit(1)
    if not os.path.exists(args.reference):
        print(f"Error: Reference file not found: {args.reference}")
        sys.exit(1)
        
    print("Reading observed Voynich text...")
    with open(args.voynich, "r", encoding="utf-8", errors="ignore") as f:
        voy_text = f.read().strip()
    voy_words = voy_text.split()
    print(f"Observed Voynich words: {len(voy_words)}")
    
    print("Reading reference plaintext corpus...")
    with open(args.reference, "r", encoding="utf-8", errors="ignore") as f:
        ref_text = f.read().strip()
    ref_words = ref_text.split()
    print(f"Reference corpus words: {len(ref_words)}")
    
    print(f"\nRunning Monte Carlo Naibbe Simulation ({args.seeds} seeds)...")
    simulator = MonteCarloSimulator(voy_words)
    stats = simulator.run_simulation(ref_text, num_seeds=args.seeds, unambiguous=not args.ambiguous)
    
    print("\n" + "=" * 115)
    print(f"{'Metric':<20} | {'Observed':<10} | {'Sim Mean':<10} | {'Sim StdDev':<10} | {'95% CI':<20} | {'Z-Score':<10} | {'Outside CI'}")
    print("-" * 115)
    
    for metric, m_stats in stats.items():
        ci_str = f"[{m_stats['ci_lower']:.4f}, {m_stats['ci_upper']:.4f}]"
        outside_str = "YES" if m_stats["outside_ci"] else "NO"
        print(f"{metric:<20} | {m_stats['observed']:<10.4f} | {m_stats['mean']:<10.4f} | {m_stats['std_dev']:<10.4f} | {ci_str:<20} | {m_stats['z_score']:<10.2f} | {outside_str}")
        
    print("=" * 115)

if __name__ == "__main__":
    main()
