# Assignment 5 - Monoalphabetic Substitution Cipher Cryptanalysis

## Course: Cryptography Laboratory (22CPP307) | Group 10

### Language: C++

---

## How to Compile and Run

```bash
# Compile
g++ -o src/mono_cipher.exe src/mono_cipher.cpp -std=c++11

# Run (from mono_substitution_attack folder)
cd attacks/mono_substitution_attack
src/mono_cipher.exe
```

---

## What This Program Does

1. Loads plaintext from `plaintext/source_text.txt` (Page 40 of Katz & Lindell)
2. Generates a **random monoalphabetic key** and encrypts the text
3. Saves ciphertext to `outputs/ciphertext.txt`
4. Provides an interactive menu for **step-by-step cryptanalysis**

---

## Menu Options

| Option | Function | What It Does |
|:------:|:---------|:-------------|
| 1 | `frequency_analysis()` | Count each letter, show frequency %, sort by most frequent |
| 2 | `word_frequency_analysis()` | Show 1-letter, 2-letter, 3-letter, and most repeated words |
| 3 | `pattern_analysis()` | Find words with repeated letter patterns (e.g., THAT = 0.1.2.0) |
| 4 | `apply_substitution()` | Map a cipher letter to a plain letter |
| 5 | Remove Substitution | Undo a mapping |
| 6 | `display_partial_plaintext()` | Show current progress — solved letters and dots for unsolved |
| 7 | Auto-Solve | Initial guess using frequency matching |
| 8 | `verify_solution()` | Compare recovered text with original, show accuracy % |
| 9 | Reset | Clear all substitutions and start over |

---

## Folder Structure

```
mono_substitution_attack/
├── src/
│   └── mono_cipher.cpp          <- Main C++ program (all 6 functions)
├── plaintext/
│   └── source_text.txt          <- Original text from textbook (Page 40)
├── outputs/
│   └── ciphertext.txt           <- Generated encrypted text
├── screenshots/                 <- Terminal screenshots
├── reports/                     <- Lab report
└── README.md                    <- This file
```

---

## Required Functions Implemented

1. **frequency_analysis()** — Counts frequency of each ciphertext letter, shows percentage, bar chart, and comparison with standard English frequency order
2. **word_frequency_analysis()** — Extracts all words, groups by length (1-letter, 2-letter, 3-letter), shows top 15 most frequent words
3. **pattern_analysis()** — Computes letter patterns for each word (e.g., HELLO = 0.1.2.2.3), finds words with repeated letters
4. **apply_substitution()** — Adds a cipher-to-plain letter mapping, warns about conflicts
5. **display_partial_plaintext()** — Shows ciphertext and partially decoded plaintext side-by-side, tracks progress percentage
6. **verify_solution()** — Compares recovered plaintext with original, calculates accuracy, shows both keys
