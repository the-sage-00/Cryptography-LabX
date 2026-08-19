"""
CryptoLabX - Chi-Square Analysis Module
Course: Cryptography Laboratory (22CPP307)
Assignment 4: Cryptanalysis of Shift Cipher

This module implements Shift Cipher cryptanalysis using the Chi-Square (χ²)
goodness-of-fit statistic against standard English letter frequencies.

Formula:
  χ² = Σ [ (Observed_i - Expected_i)² / Expected_i ]  for i = 'A' to 'Z'
  Expected_i = N * Probability_i
"""

from typing import Dict, List, Tuple
from collections import Counter
from .shift_cipher import decrypt


# Standard English letter frequency distribution (Beker & Piper, 1982)
ENGLISH_FREQUENCIES: Dict[str, float] = {
    'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702,
    'F': 0.02228, 'G': 0.02015, 'H': 0.06094, 'I': 0.06966, 'J': 0.00153,
    'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749, 'O': 0.07507,
    'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056,
    'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150, 'Y': 0.01974,
    'Z': 0.00074
}


def calculate_chi_square(text: str) -> float:
    """
    Calculate the Chi-Square statistic for a given text string against English frequencies.

    Args:
        text: Candidate decrypted plaintext.

    Returns:
        Chi-Square score (lower is better, 0.0 = perfect match).
    """
    letters_only = [ch.upper() for ch in text if ch.isalpha()]
    total_letters = len(letters_only)

    if total_letters == 0:
        return float('inf')

    counts = Counter(letters_only)
    chi_square_val = 0.0

    for letter, probability in ENGLISH_FREQUENCIES.items():
        observed = counts.get(letter, 0)
        expected = total_letters * probability
        if expected > 0:
            chi_square_val += ((observed - expected) ** 2) / expected

    return chi_square_val


def chi_square_attack(ciphertext: str) -> Dict:
    """
    Perform cryptanalysis on Shift Cipher using Chi-Square Analysis.

    Args:
        ciphertext: The encrypted text to analyze.

    Returns:
        Dictionary containing predicted_key, predicted_plaintext, min_chi_square, and all_candidates.
    """
    candidates = []
    best_key = 0
    min_chi_square = float('inf')
    best_plaintext = ""

    for key in range(26):
        decrypted = decrypt(ciphertext, key)
        chi_score = calculate_chi_square(decrypted)

        candidates.append({
            "key": key,
            "decrypted": decrypted,
            "chi_square": chi_score
        })

        if chi_score < min_chi_square:
            min_chi_square = chi_score
            best_key = key
            best_plaintext = decrypted

    return {
        "predicted_key": best_key,
        "predicted_plaintext": best_plaintext,
        "chi_square": min_chi_square,
        "candidates": candidates
    }


if __name__ == "__main__":
    from .shift_cipher import encrypt

    test_msg = "CHI SQUARE ANALYSIS EVALUATES LETTER FREQUENCIES TO PREDICT THE KEY ACCURATELY"
    actual_k = 18
    c_text = encrypt(test_msg, actual_k)

    res = chi_square_attack(c_text)
    print(f"Actual Key   : {actual_k}")
    print(f"Predicted Key: {res['predicted_key']}")
    print(f"Decrypted    : {res['predicted_plaintext']}")
    print(f"Chi-Square   : {res['chi_square']:.4f}")
