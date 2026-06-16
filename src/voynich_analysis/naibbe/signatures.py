import math
from collections import Counter
from typing import Dict, List, Set, Tuple, Union, Any

def _clean_words(text_or_list: Union[str, List[str]]) -> List[str]:
    """
    Cleans words by converting to list of words and stripping EVA brackets < and >
    to analyze the underlying character graphemes.
    
    Args:
        text_or_list: A space-separated string of words or a list of words.
        
    Returns:
        List of cleaned, non-empty words.
    """
    if isinstance(text_or_list, str):
        words = text_or_list.split()
    else:
        words = list(text_or_list)
        
    cleaned_words = []
    for w in words:
        cw = w.replace('<', '').replace('>', '').strip()
        if cw:
            cleaned_words.append(cw)
    return cleaned_words

def compute_sig1(text_or_list: Union[str, List[str]]) -> float:
    """
    Sig1: E->S transition rate.
    
    Identifies start-preferring (S) and end-preferring (E) classes using a 2:1 ratio
    based on initial/final character frequencies. Returns the percentage of consecutive
    word boundaries where an E-preferring character is followed by an S-preferring character.
    
    Args:
        text_or_list: A string or list of words.
        
    Returns:
        Transition rate (between 0.0 and 1.0).
    """
    words = _clean_words(text_or_list)
    if len(words) < 2:
        return 0.0
        
    C_start = Counter()
    C_end = Counter()
    alphabet = set()
    
    for w in words:
        C_start[w[0]] += 1
        C_end[w[-1]] += 1
        alphabet.update(w)
        
    S_pref = set()
    E_pref = set()
    
    for char in alphabet:
        c_s = C_start[char]
        c_e = C_end[char]
        if c_s >= 2 * c_e and c_s > 0:
            S_pref.add(char)
        elif c_e >= 2 * c_s and c_e > 0:
            E_pref.add(char)
            
    e_to_s_count = 0
    total_transitions = len(words) - 1
    
    for i in range(total_transitions):
        w_curr = words[i]
        w_next = words[i+1]
        if w_curr[-1] in E_pref and w_next[0] in S_pref:
            e_to_s_count += 1
            
    return e_to_s_count / total_transitions

def compute_sig2(text_or_list: Union[str, List[str]]) -> Dict[str, Any]:
    """
    Sig2: Bilateral positional extremity.
    
    Identifies characters with start/end boundary ratios >= 100:1.
    Returns a dictionary indicating the list of extreme start and extreme end characters,
    and a boolean flag indicating if extreme characters exist in BOTH categories.
    
    Args:
        text_or_list: A string or list of words.
        
    Returns:
        Dict with "extreme_start", "extreme_end", and "present" (bool).
    """
    words = _clean_words(text_or_list)
    if not words:
        return {"extreme_start": [], "extreme_end": [], "present": False}
        
    C_start = Counter()
    C_end = Counter()
    alphabet = set()
    
    for w in words:
        C_start[w[0]] += 1
        C_end[w[-1]] += 1
        alphabet.update(w)
        
    extreme_start = []
    extreme_end = []
    
    for char in alphabet:
        c_s = C_start[char]
        c_e = C_end[char]
        if c_s == 0 and c_e == 0:
            continue
            
        if c_e == 0:
            ratio = float('inf')
        elif c_s == 0:
            ratio = float('inf')
        else:
            ratio = max(c_s, c_e) / min(c_s, c_e)
            
        if ratio >= 100.0:
            if c_s > c_e:
                extreme_start.append(char)
            else:
                extreme_end.append(char)
                
    present = len(extreme_start) > 0 and len(extreme_end) > 0
    return {
        "extreme_start": sorted(extreme_start),
        "extreme_end": sorted(extreme_end),
        "present": present
    }

def compute_sig3(text_or_list: Union[str, List[str]]) -> float:
    """
    Sig3: Cross-boundary Mutual Information (in bits).
    
    Computes character-level mutual information between the final character of
    word w_i and the first character of word w_{i+1}.
    
    Args:
        text_or_list: A string or list of words.
        
    Returns:
        Mutual information in bits.
    """
    words = _clean_words(text_or_list)
    N = len(words) - 1
    if N <= 0:
        return 0.0
        
    X = [w[-1] for w in words[:-1]]
    Y = [w[0] for w in words[1:]]
    
    C_X = Counter(X)
    C_Y = Counter(Y)
    C_XY = Counter(zip(X, Y))
    
    mi = 0.0
    for (x, y), count in C_XY.items():
        p_xy = count / N
        p_x = C_X[x] / N
        p_y = C_Y[y] / N
        mi += p_xy * math.log2(p_xy / (p_x * p_y))
        
    return mi

def _compute_zipf_stats(counts: Counter) -> Dict[str, float]:
    """Helper to compute CV and R^2 of power-law fit on rank-frequency."""
    freqs = sorted([c for c in counts.values() if c > 0], reverse=True)
    if not freqs:
        return {"r2": 0.0, "cv": 0.0}
        
    mean = sum(freqs) / len(freqs)
    var = sum((f - mean)**2 for f in freqs) / len(freqs)
    std_dev = math.sqrt(var)
    cv = std_dev / mean if mean > 0 else 0.0
    
    k = len(freqs)
    if k <= 2:
        return {"r2": 1.0, "cv": cv}
        
    x = [math.log(r) for r in range(1, k + 1)]
    y = [math.log(f) for f in freqs]
    
    mean_x = sum(x) / k
    mean_y = sum(y) / k
    
    num = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(k))
    den = sum((x[i] - mean_x)**2 for i in range(k))
    
    b = num / den if den > 0 else 0.0
    a = mean_y - b * mean_x
    
    ss_tot = sum((y[i] - mean_y)**2 for i in range(k))
    ss_res = sum((y[i] - (a + b * x[i]))**2 for i in range(k))
    
    r2 = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 0.0
    return {"r2": r2, "cv": cv}

def compute_sig4(text_or_list: Union[str, List[str]]) -> Dict[str, float]:
    """
    Sig4: Zipfian boundary distributions.
    
    Computes R^2 (fit of rank-frequency log-log regression) and Coefficient
    of Variation (CV) for word-initial and word-final character distributions.
    
    Args:
        text_or_list: A string or list of words.
        
    Returns:
        A dictionary with "start_r2", "start_cv", "end_r2", and "end_cv".
    """
    words = _clean_words(text_or_list)
    if not words:
        return {"start_r2": 0.0, "start_cv": 0.0, "end_r2": 0.0, "end_cv": 0.0}
        
    C_start = Counter()
    C_end = Counter()
    for w in words:
        C_start[w[0]] += 1
        C_end[w[-1]] += 1
        
    start_stats = _compute_zipf_stats(C_start)
    end_stats = _compute_zipf_stats(C_end)
    
    return {
        "start_r2": start_stats["r2"],
        "start_cv": start_stats["cv"],
        "end_r2": end_stats["r2"],
        "end_cv": end_stats["cv"]
    }
