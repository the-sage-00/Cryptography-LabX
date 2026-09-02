"""
CryptoLabX - Shift Cipher Cryptanalysis Main Driver
Course: Cryptography Laboratory (22CPP307)
Assignment 4: Cryptanalysis of Shift Cipher

Runs automated evaluation across test cases, generates comparison table,
saves outputs, and provides an interactive CLI for testing.
"""

import os
import json
import sys
from typing import List, Dict

# Ensure package imports work regardless of execution method
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from shift_cipher import encrypt, decrypt
from brute_force_dictionary import dictionary_attack
from chi_square_attack import chi_square_attack


TEST_CASES_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "testcases", "test_cases.json"
)
OUTPUT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "outputs", "results_table.txt"
)


def run_automated_tests() -> List[Dict]:
    """Run cryptanalysis across all predefined test cases and return results."""
    if not os.path.exists(TEST_CASES_PATH):
        print(f"[!] Test cases file not found at: {TEST_CASES_PATH}")
        return []

    with open(TEST_CASES_PATH, "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    results = []
    print("\n" + "=" * 90)
    print("      CRYPTANALYSIS OF SHIFT CIPHER: AUTOMATED EXPERIMENTAL EVALUATION")
    print("=" * 90)

    for tc in test_cases:
        tc_id = tc["id"]
        desc = tc["description"]
        plaintext = tc["plaintext"]
        actual_key = tc["key"]

        ciphertext = encrypt(plaintext, actual_key)

        dict_res = dictionary_attack(ciphertext)
        chi_res = chi_square_attack(ciphertext)

        dict_key = dict_res["predicted_key"]
        chi_key = chi_res["predicted_key"]

        dict_correct = (dict_key == actual_key)
        chi_correct = (chi_key == actual_key)

        results.append({
            "id": tc_id,
            "description": desc,
            "actual_key": actual_key,
            "dict_key": dict_key,
            "chi_key": chi_key,
            "dict_correct": "YES" if dict_correct else "NO",
            "chi_correct": "YES" if chi_correct else "NO",
            "dict_plaintext": dict_res["predicted_plaintext"],
            "chi_plaintext": chi_res["predicted_plaintext"],
            "ciphertext": ciphertext
        })

    return results


SHORT_LABELS = {
    1: "Normal (spaces)",
    2: "Long text",
    3: "Short (3 words)",
    4: "No spaces",
    5: "Rare letters",
}

def print_and_save_results_table(results: List[Dict]):
    """Format and display the results table and save to outputs/results_table.txt."""
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    header  = f"| {'Test Case':<18} | {'Actual Key':<11} | {'Dict Key':<9} | {'Chi-Sq Key':<11} | {'Dict OK':<8} | {'Chi-Sq OK':<10} |"
    divider = "+" + "-" * 20 + "+" + "-" * 13 + "+" + "-" * 11 + "+" + "-" * 13 + "+" + "-" * 10 + "+" + "-" * 12 + "+"

    table_lines = []
    table_lines.append(divider)
    table_lines.append(header)
    table_lines.append(divider)

    for r in results:
        label = SHORT_LABELS.get(r["id"], f"Test {r['id']}")
        row = f"| {label:<18} | {r['actual_key']:<11} | {r['dict_key']:<9} | {r['chi_key']:<11} | {r['dict_correct']:<8} | {r['chi_correct']:<10} |"
        table_lines.append(row)

    table_lines.append(divider)

    table_str = "\n".join(table_lines)
    print("\nSUMMARY RESULTS TABLE:")
    print(table_str)

    # Detailed report section
    detail_lines = ["\nDETAILED TEST CASE BREAKDOWN:"]
    for r in results:
        detail_lines.append(f"\n--- Test Case {r['id']}: {r['description']} ---")
        detail_lines.append(f"  Actual Key      : {r['actual_key']}")
        detail_lines.append(f"  Ciphertext      : {r['ciphertext']}")
        detail_lines.append(f"  Dictionary Key  : {r['dict_key']} (Correct: {r['dict_correct']})")
        detail_lines.append(f"  Dict Plaintext  : {r['dict_plaintext']}")
        detail_lines.append(f"  Chi-Square Key  : {r['chi_key']} (Correct: {r['chi_correct']})")
        detail_lines.append(f"  Chi Plaintext   : {r['chi_plaintext']}")

    full_output = table_str + "\n" + "\n".join(detail_lines)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(full_output)

    print(f"\n[+] Results table and detailed report saved to: {OUTPUT_PATH}")


def interactive_menu():
    """Interactive CLI menu for custom text testing."""
    while True:
        print("\n" + "=" * 60)
        print("    CRYPTO LAB X -- SHIFT CIPHER CRYPTANALYSIS TOOLKIT")
        print("=" * 60)
        print("  [1] Run Automated Test Suite (5 Test Cases)")
        print("  [2] Custom Encryption & Cryptanalysis")
        print("  [3] Attack Given Ciphertext Directly")
        print("  [4] Exit")
        print("=" * 60)

        choice = input("  Select an option (1-4): ").strip()

        if choice == "1":
            results = run_automated_tests()
            print_and_save_results_table(results)
        elif choice == "2":
            pt = input("\n  Enter Plaintext: ").strip()
            try:
                k = int(input("  Enter Key (0-25): ").strip())
            except ValueError:
                print("  [!] Key must be an integer between 0 and 25.")
                continue

            ct = encrypt(pt, k)
            print(f"\n  [+] Ciphertext: {ct}")

            d_res = dictionary_attack(ct)
            c_res = chi_square_attack(ct)

            print(f"\n  --- Dictionary Attack ---")
            d_correct = "YES" if d_res["predicted_key"] == k else "NO"
            print(f"  Predicted Key: {d_res['predicted_key']} | Correct: {d_correct}")
            print(f"  Plaintext    : {d_res['predicted_plaintext']}")

            print(f"\n  --- Chi-Square Attack ---")
            c_correct = "YES" if c_res["predicted_key"] == k else "NO"
            print(f"  Predicted Key: {c_res['predicted_key']} | Correct: {c_correct}")
            print(f"  Plaintext    : {c_res['predicted_plaintext']}")
        elif choice == "3":
            ct = input("\n  Enter Ciphertext: ").strip()
            d_res = dictionary_attack(ct)
            c_res = chi_square_attack(ct)

            print(f"\n  --- Dictionary Attack Result ---")
            print(f"  Predicted Key: {d_res['predicted_key']}")
            print(f"  Plaintext    : {d_res['predicted_plaintext']}")

            print(f"\n  --- Chi-Square Attack Result ---")
            print(f"  Predicted Key: {c_res['predicted_key']}")
            print(f"  Plaintext    : {c_res['predicted_plaintext']}")
        elif choice == "4":
            print("\n  Exiting Cryptanalysis Toolkit. Goodbye!\n")
            break
        else:
            print("  [!] Invalid choice. Please select 1-4.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        results = run_automated_tests()
        print_and_save_results_table(results)
    else:
        results = run_automated_tests()
        print_and_save_results_table(results)
        interactive_menu()
