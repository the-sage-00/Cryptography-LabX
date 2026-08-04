"""
CryptoLabX - File Analyzer
Reads a text file and displays: number of characters, words,
lines, unique characters, and letter frequency.
"""

import os
from collections import Counter

DATASETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "datasets")


def list_dataset_files():
    """List all .txt files available in the datasets folder."""
    if not os.path.exists(DATASETS_DIR):
        return []
    return [f for f in os.listdir(DATASETS_DIR) if f.endswith(".txt")]


def analyze_file(filepath):
    """
    Analyze a text file and return its statistics.

    Args:
        filepath: Path to the text file.

    Returns:
        dict with characters, words, lines, unique_chars, letter_frequency.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()
    words = content.split()
    unique_chars = sorted(set(content))

    letters = [ch.lower() for ch in content if ch.isalpha()]
    letter_freq = dict(sorted(Counter(letters).items()))

    return {
        "characters": len(content),
        "words": len(words),
        "lines": len(lines),
        "unique_chars": unique_chars,
        "letter_frequency": letter_freq,
    }


def display_analysis(filename, stats):
    """Print the analysis results in a formatted layout."""
    print(f"\n{'=' * 50}")
    print(f"  FILE ANALYSIS: {filename}")
    print(f"{'=' * 50}")
    print(f"  Total Characters  : {stats['characters']}")
    print(f"  Total Words       : {stats['words']}")
    print(f"  Total Lines       : {stats['lines']}")
    print(f"  Unique Characters : {len(stats['unique_chars'])}")
    print(f"\n  {'─' * 40}")
    print(f"  LETTER FREQUENCY")
    print(f"  {'─' * 40}")
    for letter, count in stats["letter_frequency"].items():
        bar = "█" * min(count, 30)
        print(f"    {letter} : {count:4d}  {bar}")
    print(f"{'=' * 50}\n")


def run_file_analysis():
    """Interactive workflow: list files, pick one, analyze and display."""
    files = list_dataset_files()
    if not files:
        print("\n  No text files found in datasets/ folder.\n")
        return

    print(f"\n  Available files in datasets/:")
    print(f"  {'─' * 35}")
    for i, fname in enumerate(files, 1):
        print(f"    [{i}] {fname}")
    print(f"    [0] Back to main menu")

    try:
        sel = input("\n  Select a file to analyze: ").strip()
        idx = int(sel)
        if idx == 0:
            return
        if 1 <= idx <= len(files):
            filepath = os.path.join(DATASETS_DIR, files[idx - 1])
            stats = analyze_file(filepath)
            display_analysis(files[idx - 1], stats)
        else:
            print("  Invalid selection.\n")
    except (ValueError, IndexError):
        print("  Invalid input.\n")
