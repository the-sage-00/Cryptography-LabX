"""
CryptoLabX - Vigenère Cipher Cryptanalysis Driver
Course: Cryptography Laboratory (22CPP307)
Assignment 6: Cryptanalysis of Vigenère Cipher using Kasiski Examination and Frequency Analysis
Group: 10 (Even Group Number)

Runs Kasiski examination, calculates Index of Coincidence, estimates key length,
performs unigram frequency analysis per group, reconstructs key, decrypts ciphertext,
and validates through re-encryption.
"""

import os
import sys
import json
from typing import Dict

# Fix Windows terminal encoding
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Ensure local package imports work regardless of current working directory
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from vigenere_attack import (
    clean_ciphertext,
    find_repeated_patterns,
    calculate_distances,
    find_factors,
    kasiski_analysis,
    calculate_ic,
    split_into_groups,
    frequency_analysis,
    find_shift,
    find_key,
    vigenere_decrypt,
    vigenere_encrypt,
    verify
)

DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "testcases", "ciphertexts.json"
)
OUTPUT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "outputs", "results_table.txt"
)


def print_banner():
    print("=" * 78)
    print("      CRYPTANALYSIS OF VIGENÈRE CIPHER (KASISKI + FREQUENCY ANALYSIS)")
    print("         Course: Cryptography Laboratory (22CPP307) | Group: 10")
    print("=" * 78)


def analyze_ciphertext(ciphertext_raw: str, label: str = "Target Ciphertext", max_key_len: int = 20) -> Dict:
    """
    Perform complete cryptanalytic pipeline on a ciphertext:
    1. Preprocessing / normalization
    2. Kasiski examination
    3. Index of Coincidence calculation
    4. Group partitioning
    5. Frequency analysis per group
    6. Key extraction
    7. Decryption
    8. Verification by re-encryption
    """
    clean_ct = clean_ciphertext(ciphertext_raw)
    n = len(clean_ct)

    print(f"\n[+] Analyzing: {label}")
    print(f"    Raw ciphertext length : {len(ciphertext_raw)} characters")
    print(f"    Normalized length     : {n} uppercase characters")

    # 1. Kasiski Test
    print("\n" + "-" * 78)
    print("1. KASISKI EXAMINATION (Repeated Patterns & Distance Analysis)")
    print("-" * 78)
    patterns = find_repeated_patterns(clean_ct, min_len=3, max_len=5)
    print(f"    Total repeated patterns (length 3-5) found: {len(patterns)}")

    # Show top 8 sample patterns
    print("\n    Sample Repeated Patterns and Positions:")
    for pat, pos in list(patterns.items())[:8]:
        dists = [pos[j+1] - pos[j] for j in range(len(pos)-1)]
        print(f"      Pattern '{pat}' (len {len(pat)}) -> positions: {pos[:4]} | distances: {dists[:3]}")

    distances = calculate_distances(patterns)
    factors = find_factors(distances, max_factor=max_key_len)

    ranked_factors = sorted(factors.items(), key=lambda x: x[1], reverse=True)
    print("\n    Kasiski Candidate Key Lengths (Ranked by Factor Counts):")
    print(f"      {'Key Length':<12} {'Factor Matches':<16} {'Bar Indicator'}")
    print("      " + "-" * 45)
    for length, count in ranked_factors[:8]:
        bar = "#" * min(30, count // 2)
        print(f"      {length:<12} {count:<16} {bar}")

    # 2. Index of Coincidence (IC) Analysis
    print("\n" + "-" * 78)
    print("2. INDEX OF COINCIDENCE (IC) EVALUATION")
    print("   (Standard English: ~0.068 | Random Polyalphabetic: ~0.038)")
    print("-" * 78)

    ic_table = []
    best_klen = 1
    best_ic_diff = float('inf')

    print(f"    {'Key Length':<12} {'Average IC':<15} {'Deviation from English (0.068)'}")
    print("    " + "-" * 55)

    for klen in range(1, max_key_len + 1):
        groups = split_into_groups(clean_ct, klen)
        avg_ic = sum(calculate_ic(g) for g in groups) / klen
        diff = abs(avg_ic - 0.068)
        ic_table.append((klen, avg_ic, diff))
        marker = " <== BEST FIT (ENGLISH)" if avg_ic >= 0.062 else ""
        print(f"    {klen:<12} {avg_ic:<15.4f} {diff:<25.4f}{marker}")

        # Pick candidate with high IC closest to 0.068
        if avg_ic >= 0.060 and diff < best_ic_diff:
            best_ic_diff = diff
            best_klen = klen

    # If no candidate >= 0.060, take highest IC
    if best_klen == 1:
        best_klen = max(ic_table[1:], key=lambda x: x[1])[0]

    estimated_key_length = best_klen
    print(f"\n[>>>] FINAL ESTIMATED KEY LENGTH: {estimated_key_length}")

    # 3. Partitioning & Group Frequency Analysis
    print("\n" + "-" * 78)
    print(f"3. GROUP PARTITIONING & CAESAR SHIFT FREQUENCY ANALYSIS (L = {estimated_key_length})")
    print("-" * 78)

    groups = split_into_groups(clean_ct, estimated_key_length)
    recovered_key_chars = []
    group_shifts = []

    print(f"    {'Group #':<10} {'Group Size':<12} {'Shift':<8} {'Key Char':<10} {'Min Chi-Square'}")
    print("    " + "-" * 55)

    for i, g in enumerate(groups):
        shift, key_char, chi_score = find_shift(g)
        recovered_key_chars.append(key_char)
        group_shifts.append((shift, key_char, chi_score))
        print(f"    Group {i+1:<4} {len(g):<12} {shift:<8} {key_char:<10} {chi_score:.2f}")

    recovered_key = ''.join(recovered_key_chars)
    print(f"\n[>>>] RECOVERED PROBABLE KEY: {recovered_key}")

    # 4. Decryption
    recovered_pt = vigenere_decrypt(clean_ct, recovered_key)

    # 5. Verification
    is_verified = verify(clean_ct, recovered_pt, recovered_key)

    print("\n" + "-" * 78)
    print("4. RE-ENCRYPTION & CRYPTANALYTIC VERIFICATION")
    print("-" * 78)
    print(f"    Re-encryption Match    : {'YES [100% MATCH]' if is_verified else 'NO [FAILED]'}")
    print(f"    Ciphertext Recovered   : {'Exact match to original' if is_verified else 'Mismatch'}")

    print("\n" + "-" * 78)
    print("5. RECOVERED PLAINTEXT (Preview)")
    print("-" * 78)
    print("    First 300 characters:")
    print(f"    {recovered_pt[:300]}")
    print("\n    Last 200 characters:")
    print(f"    {recovered_pt[-200:]}")

    # Build structured return data
    return {
        "label": label,
        "clean_ct_len": n,
        "estimated_key_length": estimated_key_length,
        "recovered_key": recovered_key,
        "verified": is_verified,
        "groups_count": len(groups),
        "group_shifts": group_shifts,
        "plaintext_preview": recovered_pt[:300],
        "full_plaintext": recovered_pt,
        "clean_ct": clean_ct
    }


def display_frequency_table_sample(group_text: str, group_num: int):
    """Display detailed A-Z frequency table for a selected group."""
    counts = frequency_analysis(group_text)
    total = len(group_text)

    print(f"\n--- Detailed Frequency Table for Group {group_num} (Size: {total}) ---")
    print(f"{'Letter':<8} {'Count':<8} {'Frequency %':<14} {'Bar'}")
    print("-" * 45)
    for i in range(26):
        ch = chr(ord('A') + i)
        cnt = counts[ch]
        pct = (cnt / total * 100) if total > 0 else 0
        bar = "#" * int(pct)
        print(f"{ch:<8} {cnt:<8} {pct:<14.2f} {bar}")


def save_summary_output(result: Dict):
    """Save formatted results table and detailed findings to outputs/results_table.txt."""
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    lines = [
        "=" * 80,
        "      CRYPTANALYSIS OF VIGENÈRE CIPHER — EXPERIMENTAL RESULTS REPORT",
        "         Course: Cryptography Laboratory (22CPP307) | Group: 10",
        "=" * 80,
        f"Target Dataset         : {result['label']}",
        f"Ciphertext Length      : {result['clean_ct_len']} letters",
        f"Estimated Key Length   : {result['estimated_key_length']}",
        f"Recovered Key          : {result['recovered_key']}",
        f"Re-encryption Verified : {'YES (100% Exact Match)' if result['verified'] else 'NO'}",
        "",
        "SUMMARY BREAKDOWN TABLE:",
        "+" + "-" * 10 + "+" + "-" * 14 + "+" + "-" * 12 + "+" + "-" * 12 + "+" + "-" * 18 + "+",
        f"| {'Group #':<8} | {'Group Size':<12} | {'Caesar Shift':<10} | {'Key Char':<10} | {'Chi-Square Min':<16} |",
        "+" + "-" * 10 + "+" + "-" * 14 + "+" + "-" * 12 + "+" + "-" * 12 + "+" + "-" * 18 + "+",
    ]

    for idx, (shift, char, chi) in enumerate(result['group_shifts']):
        lines.append(
            f"| {idx+1:<8} | {result['clean_ct_len']//result['estimated_key_length']:<12} | {shift:<10} | {char:<10} | {chi:<16.2f} |"
        )

    lines.extend([
        "+" + "-" * 10 + "+" + "-" * 14 + "+" + "-" * 12 + "+" + "-" * 12 + "+" + "-" * 18 + "+",
        "",
        "RECOVERED PLAINTEXT (FIRST 400 CHARACTERS):",
        "-" * 80,
        result['plaintext_preview'],
        "-" * 80,
        "",
        "FULL RECOVERED PLAINTEXT:",
        result['full_plaintext']
    ])

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"\n[+] Full experimental report and tables saved to:\n    {OUTPUT_PATH}")


def run_assignment():
    """Main interactive driver."""
    print_banner()

    # Load ciphertexts from JSON
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        print(f"[!] Testcases file missing at: {DATA_PATH}")
        return

    while True:
        print("\n" + "=" * 60)
        print("  ASSIGNMENT 6 INTERACTIVE MENU:")
        print("=" * 60)
        print("  [1] Run Cryptanalysis on Group 10 Dataset (Ciphertext-2, Even)")
        print("  [2] Run Cryptanalysis on Ciphertext-1 (Odd Group Numbers)")
        print("  [3] Inspect Detailed Frequency Table for a Specific Group")
        print("  [4] Custom Ciphertext Cryptanalysis")
        print("  [5] Exit")
        print("=" * 60)

        choice = input("  Select an option (1-5): ").strip()

        if choice == "1":
            ct = data["ciphertext_2_even"]["ciphertext"]
            res = analyze_ciphertext(ct, label="Group 10 (Even Group Numbers) — Ciphertext-2")
            save_summary_output(res)

        elif choice == "2":
            ct = data["ciphertext_1_odd"]["ciphertext"]
            res = analyze_ciphertext(ct, label="Ciphertext-1 (Odd Group Numbers)")
            save_summary_output(res)

        elif choice == "3":
            ct = data["ciphertext_2_even"]["ciphertext"]
            clean_ct = clean_ciphertext(ct)
            klen_str = input("  Enter Key Length (default 12 for Group 10): ").strip()
            klen = int(klen_str) if klen_str.isdigit() else 12
            groups = split_into_groups(clean_ct, klen)

            g_idx_str = input(f"  Enter Group Number to inspect (1 to {klen}): ").strip()
            g_idx = int(g_idx_str) if g_idx_str.isdigit() and 1 <= int(g_idx_str) <= klen else 1
            display_frequency_table_sample(groups[g_idx - 1], g_idx)

        elif choice == "4":
            custom_ct = input("\n  Enter or paste your ciphertext: ").strip()
            if not custom_ct:
                print("  [!] Ciphertext cannot be empty.")
                continue
            res = analyze_ciphertext(custom_ct, label="Custom User Ciphertext")
            save_summary_output(res)

        elif choice == "5":
            print("\n  Exiting Vigenère Cipher Cryptanalysis Toolkit. Goodbye!\n")
            break

        else:
            print("  [!] Invalid choice. Please choose 1 to 5.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        print_banner()
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        ct = data["ciphertext_2_even"]["ciphertext"]
        res = analyze_ciphertext(ct, label="Group 10 (Even Group Numbers) — Ciphertext-2")
        save_summary_output(res)
    else:
        run_assignment()
