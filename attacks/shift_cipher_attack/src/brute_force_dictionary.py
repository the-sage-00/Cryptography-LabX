"""
CryptoLabX - Brute-Force & Dictionary Scoring Attack Module
Course: Cryptography Laboratory (22CPP307)
Assignment 4: Cryptanalysis of Shift Cipher

This module implements Shift Cipher cryptanalysis via exhaustive key search (brute-force)
and dictionary word matching score evaluation.
"""

import os
import re
from typing import Dict, List, Tuple, Set
from .shift_cipher import decrypt


DEFAULT_DICT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "dictionary", "english_words.txt"
)


def load_dictionary(dict_path: str = DEFAULT_DICT_PATH) -> Set[str]:
    """
    Load a list of English words from a text file into a lowercase set.

    Args:
        dict_path: Path to english_words.txt file.

    Returns:
        Set of lowercase English words.
    """
    if not os.path.exists(dict_path):
        raise FileNotFoundError(f"Dictionary file not found at: {dict_path}")

    words = set()
    with open(dict_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            word = line.strip().lower()
            if word:
                words.add(word)
    return words


def dictionary_score(text: str, dictionary: Set[str]) -> Tuple[int, float]:
    """
    Calculate dictionary match score for a given text string.

    Args:
        text: Candidate decrypted plaintext.
        dictionary: Set of valid English words.

    Returns:
        Tuple of (matched_word_count, match_percentage).
    """
    # Tokenize text into words (alphabetic sequences)
    words = re.findall(r'[a-zA-Z]+', text.lower())
    if not words:
        return 0, 0.0

    matched = sum(1 for w in words if w in dictionary)
    percentage = (matched / len(words)) * 100.0
    return matched, percentage


def dictionary_attack(ciphertext: str, dict_path: str = DEFAULT_DICT_PATH) -> Dict:
    """
    Perform brute-force attack on Shift Cipher using Dictionary Scoring.

    Args:
        ciphertext: The encrypted text to analyze.
        dict_path: Path to dictionary word list.

    Returns:
        Dictionary containing predicted_key, predicted_plaintext, all_candidates, and max_score.
    """
    dictionary = load_dictionary(dict_path)
    candidates = []

    best_key = 0
    best_score = -1.0
    best_matched_count = -1
    best_plaintext = ""

    for key in range(26):
        decrypted = decrypt(ciphertext, key)
        matched_count, score_pct = dictionary_score(decrypted, dictionary)

        candidates.append({
            "key": key,
            "decrypted": decrypted,
            "matched_words": matched_count,
            "score_pct": score_pct
        })

        # Select candidate with highest matched words, breaking ties with percentage
        if (matched_count > best_matched_count) or (
            matched_count == best_matched_count and score_pct > best_score
        ):
            best_matched_count = matched_count
            best_score = score_pct
            best_key = key
            best_plaintext = decrypted

    return {
        "predicted_key": best_key,
        "predicted_plaintext": best_plaintext,
        "matched_words": best_matched_count,
        "score_pct": best_score,
        "candidates": candidates
    }


if __name__ == "__main__":
    from .shift_cipher import encrypt

    test_msg = "CRYPTANALYSIS OF SHIFT CIPHER USING DICTIONARY ATTACK IS FAST AND SIMPLE"
    actual_k = 13
    c_text = encrypt(test_msg, actual_k)

    res = dictionary_attack(c_text)
    print(f"Actual Key   : {actual_k}")
    print(f"Predicted Key: {res['predicted_key']}")
    print(f"Decrypted    : {res['predicted_plaintext']}")
    print(f"Score (%)    : {res['score_pct']:.2f}%")
