# Voynich Statistical Analysis Toolkit

A Python library for computational and statistical analysis of the Voynich Manuscript using Shannon entropy metrics, Monte Carlo simulations, and positional character signatures (Naibbe replication / Parisel signatures).

This toolkit provides researchers and data scientists with standard, reproducible implementations of statistical models used to analyze the linguistic and structural features of the Voynich Manuscript.

---

## Features

- **Shannon Entropy Analysis**:
  - Calculate first-order ($H_1$) and second-order ($H_2$) Shannon entropy.
  - Calculate conditional character entropy ($H_{cond}$).
  - Estimate the $R$-ratio ($H_2 / H_1^2$) and evaluate its statistical significance against a shuffle-null distribution (Monte Carlo shuffling).
- **Naibbe Encoder**:
  - A faithful replication of the Naibbe encoding mechanism (simulating manual card drawing and dice-rolling respacing algorithms).
  - Configurable unigram/bigram ambiguity checks.
- **Parisel Positional Signatures**:
  - **Sig1**: E-to-S transition rates between word boundaries.
  - **Sig2**: Bilateral Positional Extremity (ratio of character positions at start vs. end of words).
  - **Sig3**: Cross-boundary Mutual Information (character associations across word spaces).
  - **Sig4**: Zipfian boundary distributions (log-log regression fit $R^2$ and Coefficient of Variation for word-initial and word-final characters).
- **Monte Carlo Simulator**:
  - Orchestrate multiple randomized encoding runs to compare observed Voynich characteristics against synthetic ciphers.

---

## Installation

### From Source

Clone the repository and install the package in editable mode:

```bash
git clone https://github.com/yourusername/voynich-entropy-analysis.git
cd voynich-entropy-analysis
pip install -e .
```

To install development dependencies (e.g. for testing):

```bash
pip install -e ".[dev]"
```

---

## Quickstart

Run the built-in demonstration script to verify the installation:

```bash
python examples/run_analysis.py
```

### CLI Interface

The package installs a command-line script called `voynich-analysis`.

#### 1. Running Entropy Analysis

Calculate character entropy on a text file and evaluate its significance:

```bash
voynich-analysis entropy path/to/voynich.txt --shuffles 500 --seed 42
```

#### 2. Running Monte Carlo Simulation

Compare a reference text (e.g. Pliny) to observed Voynich text using Naibbe encryption over 100 seeds:

```bash
voynich-analysis simulate --voynich path/to/voynich.txt --reference path/to/pliny.txt --seeds 100
```

---

## API Usage

### Shannon Entropy & Shuffle Null

```python
from voynich_analysis.entropy import analyze_entropy_significance

# Prepare text characters
text = "The quick brown fox jumps..."
chars = [c.lower() for c in text if c.isalpha()]

# Compute metrics and compare with 500 shuffles
results = analyze_entropy_significance(chars, n_shuffles=500, seed=42)

print(f"Observed R-ratio: {results['R_observed']:.4f}")
print(f"Z-Score         : {results['z_score']:.2f}")
print(f"Empirical P-val : {results['percentile']}%")
```

### Naibbe Encryption

```python
from voynich_analysis.naibbe import NaibbeEncoder

encoder = NaibbeEncoder(seed=42)

# Normalize and encode a document
plaintext = "In nova fert animus mutatas dicere formas..."
ciphertext = encoder.encode(plaintext, unambiguous=True)

print(ciphertext)
# Output: "<ol> <chedy> <daiin> <shedy> <qokaiin> ..."
```

### Positional Signatures

```python
from voynich_analysis.naibbe import compute_sig1, compute_sig2

words = ["<ol>", "<chedy>", "<daiin>", "<shedy>"]

# E-to-S transition rate
sig1 = compute_sig1(words)

# Bilateral positional extremity
sig2 = compute_sig2(words)
print("Is bilateral extremity present?", sig2["present"])
```

---

## Mathematical Background

### 1. Shannon Entropy & R-Ratio

The first-order entropy $H_1$ measures the average uncertainty of single characters:

$$H_1 = -\sum_{x \in \mathcal{X}} p(x) \log_2 p(x)$$

The second-order entropy $H_2$ measures the uncertainty of character bigrams:

$$H_2 = -\sum_{x, y \in \mathcal{X}} p(x,y) \log_2 p(x,y)$$

The $R$-ratio normalized for character distribution is defined as:

$$R = \frac{H_2}{H_1^2}$$

To check if the observed $R$-ratio is significantly different from a random arrangement with the same unigram frequency, we shuffle the characters randomly $N$ times and compute the $Z$-score:

$$Z = \frac{R_{\text{observed}} - \mu_{R_{\text{null}}}}{\sigma_{R_{\text{null}}}}$$

### 2. Cross-boundary Mutual Information (Sig3)

Measures how much information the last letter of a word tells us about the first letter of the next word:

$$I(X; Y) = \sum_{x \in \mathcal{X}} \sum_{y \in \mathcal{Y}} p(x,y) \log_2 \frac{p(x,y)}{p(x)p(y)}$$

---

## Testing

Run tests with `pytest`:

```bash
pytest
```
