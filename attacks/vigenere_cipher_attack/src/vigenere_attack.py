"""
CryptoLabX - Cryptanalysis of Vigenère Cipher
Course: Cryptography Laboratory (22CPP307)
Assignment 6: Kasiski Examination and Frequency Analysis
Group: 10 (Even Group Number)

Implements all required user-defined functions:
1. clean_ciphertext()
2. find_repeated_patterns()
3. calculate_distances()
4. find_factors()
5. kasiski_analysis()
6. calculate_ic()
7. split_into_groups()
8. frequency_analysis()
9. find_shift()
10. find_key()
11. vigenere_decrypt()
12. vigenere_encrypt()
13. verify()
"""

import re
from collections import Counter, defaultdict
from typing import Dict, List, Tuple


# Standard English monogram frequencies (probabilities summing to 1.0)
ENGLISH_FREQUENCIES = {
    'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253,
    'E': 0.12702, 'F': 0.02228, 'G': 0.02015, 'H': 0.06094,
    'I': 0.06966, 'J': 0.00153, 'K': 0.00772, 'L': 0.04025,
    'M': 0.02406, 'N': 0.06749, 'O': 0.07507, 'P': 0.01929,
    'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056,
    'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150,
    'Y': 0.01974, 'Z': 0.00074
}


def clean_ciphertext(ciphertext: str) -> str:
    """
    Remove spaces, newlines, numbers, and special characters.
    Normalize ciphertext to uppercase alphabetic characters (A-Z).
    """
    return re.sub(r'[^A-Za-z]', '', ciphertext).upper()


def find_repeated_patterns(ciphertext: str, min_len: int = 3, max_len: int = 5) -> Dict[str, List[int]]:
    """
    Identify repeated sequences in the ciphertext of lengths between min_len and max_len.
    Returns a dictionary mapping each pattern to the list of 0-based indices where it occurs.
    """
    clean_ct = clean_ciphertext(ciphertext)
    repeated = {}

    for length in range(min_len, max_len + 1):
        positions = defaultdict(list)
        for i in range(len(clean_ct) - length + 1):
            pattern = clean_ct[i:i + length]
            positions[pattern].append(i)

        for pattern, pos_list in positions.items():
            if len(pos_list) > 1:
                repeated[pattern] = pos_list

    return repeated


def calculate_distances(patterns: Dict[str, List[int]]) -> List[int]:
    """
    Find distances between consecutive occurrences of each repeated sequence.
    """
    distances = []
    for pattern, positions in patterns.items():
        for i in range(len(positions) - 1):
            dist = positions[i + 1] - positions[i]
            distances.append(dist)
    return distances


def find_factors(distances: List[int], max_factor: int = 20) -> Dict[int, int]:
    """
    Find factors (from 2 up to max_factor) for each distance obtained from repeated patterns.
    Returns a dictionary mapping factor -> count of occurrences.
    """
    factor_counts = defaultdict(int)
    for dist in distances:
        for factor in range(2, max_factor + 1):
            if dist % factor == 0:
                factor_counts[factor] += 1
    return dict(factor_counts)


def kasiski_analysis(ciphertext: str, min_len: int = 3, max_factor: int = 20) -> List[Tuple[int, int]]:
    """
    Use repeated patterns and their distance factors to suggest candidate key lengths.
    Returns a ranked list of tuples: (candidate_key_length, factor_frequency).
    """
    patterns = find_repeated_patterns(ciphertext, min_len=min_len)
    distances = calculate_distances(patterns)
    factors = find_factors(distances, max_factor=max_factor)

    ranked_candidates = sorted(factors.items(), key=lambda item: item[1], reverse=True)
    return ranked_candidates


def calculate_ic(text: str) -> float:
    """
    Calculate the Index of Coincidence (IC) for a given text.
    Standard English text: IC ~ 0.068
    Random polyalphabetic text: IC ~ 0.038
    Formula: IC = sum(f_i * (f_i - 1)) / (N * (N - 1))
    """
    clean_text = clean_ciphertext(text)
    n = len(clean_text)
    if n <= 1:
        return 0.0

    counts = Counter(clean_text)
    numerator = sum(count * (count - 1) for count in counts.values())
    denominator = n * (n - 1)
    return numerator / denominator


def split_into_groups(ciphertext: str, key_length: int) -> List[str]:
    """
    Divide ciphertext into groups according to candidate key length (cosets).
    Group i contains all ciphertext letters at positions where (pos % key_length) == i.
    """
    clean_ct = clean_ciphertext(ciphertext)
    groups = ['' for _ in range(key_length)]
    for idx, char in enumerate(clean_ct):
        groups[idx % key_length] += char
    return groups


def frequency_analysis(group: str) -> Dict[str, int]:
    """
    Calculate A–Z frequency count for each group.
    Returns a dictionary mapping each uppercase letter A-Z to its occurrence count.
    """
    clean_group = clean_ciphertext(group)
    counts = Counter(clean_group)
    return {chr(ord('A') + i): counts.get(chr(ord('A') + i), 0) for i in range(26)}


def find_shift(group: str) -> Tuple[int, str, float]:
    """
    Estimate the Caesar shift for a group using Chi-Square goodness-of-fit against English frequencies.
    Formula: Chi-Square = sum((Observed - Expected)^2 / Expected)
    Returns: (best_shift_int, best_key_char, minimum_chi_square_score)
    """
    clean_group = clean_ciphertext(group)
    n = len(clean_group)
    if n == 0:
        return 0, 'A', 0.0

    best_shift = 0
    best_chi = float('inf')

    for shift in range(26):
        chi_score = 0.0
        # Decrypt group with current shift candidate
        decrypted = [chr((ord(c) - ord('A') - shift) % 26 + ord('A')) for c in clean_group]
        counts = Counter(decrypted)

        for i in range(26):
            letter = chr(ord('A') + i)
            expected = n * ENGLISH_FREQUENCIES[letter]
            observed = counts.get(letter, 0)
            chi_score += ((observed - expected) ** 2) / expected

        if chi_score < best_chi:
            best_chi = chi_score
            best_shift = shift

    key_char = chr(ord('A') + best_shift)
    return best_shift, key_char, best_chi


def find_key(groups: List[str]) -> str:
    """
    Combine shifts for all groups to obtain the probable Vigenère key.
    """
    key_chars = []
    for group in groups:
        _, key_char, _ = find_shift(group)
        key_chars.append(key_char)
    return ''.join(key_chars)


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """
    Decrypt ciphertext using the recovered key.
    Formula: P_i = (C_i - K_(i % L)) mod 26
    Preserves non-alphabetic characters if present, or decodes clean string.
    """
    clean_key = clean_ciphertext(key)
    key_len = len(clean_key)
    if key_len == 0:
        return ciphertext

    decrypted = []
    key_idx = 0

    for char in ciphertext:
        if char.isalpha():
            is_lower = char.islower()
            c_val = ord(char.upper()) - ord('A')
            k_val = ord(clean_key[key_idx % key_len]) - ord('A')
            p_val = (c_val - k_val) % 26
            p_char = chr(p_val + ord('A'))
            decrypted.append(p_char.lower() if is_lower else p_char)
            key_idx += 1
        else:
            decrypted.append(char)

    return ''.join(decrypted)


def vigenere_encrypt(plaintext: str, key: str) -> str:
    """
    Re-encrypt plaintext for verification using key.
    Formula: C_i = (P_i + K_(i % L)) mod 26
    """
    clean_key = clean_ciphertext(key)
    key_len = len(clean_key)
    if key_len == 0:
        return plaintext

    encrypted = []
    key_idx = 0

    for char in plaintext:
        if char.isalpha():
            is_lower = char.islower()
            p_val = ord(char.upper()) - ord('A')
            k_val = ord(clean_key[key_idx % key_len]) - ord('A')
            c_val = (p_val + k_val) % 26
            c_char = chr(c_val + ord('A'))
            encrypted.append(c_char.lower() if is_lower else c_char)
            key_idx += 1
        else:
            encrypted.append(char)

    return ''.join(encrypted)


def verify(ciphertext: str, plaintext: str, key: str) -> bool:
    """
    Check whether re-encrypting the recovered plaintext produces the original ciphertext.
    Returns True if re-encrypted text exactly matches the cleaned ciphertext.
    """
    clean_ct = clean_ciphertext(ciphertext)
    clean_pt = clean_ciphertext(plaintext)
    re_encrypted = clean_ciphertext(vigenere_encrypt(clean_pt, key))
    return re_encrypted == clean_ct
