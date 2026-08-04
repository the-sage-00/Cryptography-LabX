# CryptoLabX Assignment 1 — Complete Learning & Viva Guide

> A simple, step-by-step explanation of everything built in **Assignment 1 (Week 1)** for **Cryptography Laboratory (22CPP307)**.

---

## 1. Executive Summary & Overview

You have been recruited as a Junior Cryptanalyst to build a modular software framework called **CryptoLabX**. 
In Week 1, the goal is **strictly to establish the foundation** — project organization, Git version control, command-line interface (CLI), file analysis, execution logging, and documentation. No cryptographic ciphers (like AES, Caesar, etc.) are implemented in Week 1.

---

## 2. Why Do We Need All These Parts?

| Component | Why It Is Needed | Real-World Analogy |
| :--- | :--- | :--- |
| **Folder Structure** | Organizes code logically so modules don't get mixed up. | A tool chest with labeled drawers. |
| **Git & GitHub** | Tracks every single change, allows rollback, and enables team collaboration. | A save point system in a video game. |
| **Menu System (CLI)** | Provides a simple interactive prompt for the user to select tasks. | A TV remote control or kiosk screen. |
| **File Analysis** | Extracts key metrics (character/word counts, letter frequencies) needed for cryptanalysis. | An X-ray scanner for text documents. |
| **Execution Logging** | Records timestamps and user actions for auditing and debugging. | A security logbook at a building entrance. |
| **Datasets** | Sample texts to test ciphers and frequency analysis algorithms in future weeks. | Practice sheets for training. |
| **README Document** | Gives anyone inspecting the repository a full picture of the software and how to run it. | An instruction manual. |

---

## 3. Detailed Task-by-Task Explanation

---

### Task 1 & 2: Git Repository & Folder Structure

#### Directory Tree:
```text
CryptoLabX/
├── classical/       ← Classical ciphers (Caesar, Vigenere, etc. - Future)
├── attacks/         ← Attack modules (Brute force, Frequency analysis - Future)
├── math/            ← Math utilities (GCD, Modular inverse, Primes - Future)
├── modern/          ← Modern ciphers (AES, DES, RSA - Future)
├── analysis/        ← Text & frequency analysis tools
│   └── file_analyzer.py
├── datasets/        ← Sample text files for cryptanalysis
├── outputs/         ← Log files and analysis output files
├── docs/            ← Documentation & lab reports
├── tests/           ← Unit tests
├── utils/           ← Helper utilities (Menu, Logger)
│   ├── menu.py
│   └── logger.py
├── main.py          ← Primary entry point
├── README.md        ← Project documentation
└── requirements.txt ← Project dependencies
```

#### Key Technical Concepts:
- **`__init__.py`**: Indicates to Python that a directory is a package, allowing functions to be imported across files (e.g., `from utils.menu import display_menu`).
- **`.gitkeep`**: Git tracks files, not empty folders. `.gitkeep` is a placeholder file to ensure empty directories are committed.
- **`.gitignore`**: Excludes temporary files (like `__pycache__` and runtime `*.log` files) from being pushed to GitHub.

---

### Task 3: Command-Line Interface (CLI)

- **Entry File**: `main.py`
- **Menu Module**: `utils/menu.py`

#### How It Works:
1. `main.py` initializes an infinite loop (`while running:`).
2. It displays the main banner and menu options:
   - `[1] Encrypt` → Displays "Coming Soon"
   - `[2] Decrypt` → Displays "Coming Soon"
   - `[3] Attack` → Displays "Coming Soon"
   - `[4] Analyze` → Triggers Task 4 File Analysis
   - `[5] Exit` → Gracefully closes the application
3. Modular design separates the UI rendering logic from the main application execution loop.

---

### Task 4: File Analysis Module

- **Implementation File**: `analysis/file_analyzer.py`

#### What Statistics Are Computed?
1. **Total Characters**: Length of the raw text string (`len(content)`).
2. **Total Words**: Length of the split word list (`len(content.split())`).
3. **Total Lines**: Number of newline breaks (`len(content.splitlines())`).
4. **Unique Characters**: Distinct characters found in the file using Python `set(content)`.
5. **Letter Frequency**: Alphabet distribution calculated using `collections.Counter`, formatted with an ASCII bar chart (`#`).

#### Why Letter Frequency Matters in Cryptography:
In English, letters appear with predictable frequencies (e.g., **E** is ~12.7%, **T** is ~9.1%). In substitution ciphers, frequency analysis allows a cryptanalyst to crack codes without knowing the key.

---

### Task 5: Execution Logger

- **Implementation File**: `utils/logger.py`
- **Output File**: `outputs/cryptolabx.log`

#### How It Works:
Whenever a user selects any option in the menu, `log_action(option_name)` records the action in append mode (`"a"`):
```text
[2026-08-04 21:37:37] Selected: Analyze
[2026-08-04 21:38:32] Selected: Exit
```

---

### Task 6: Datasets

Five text files were created inside the `datasets/` folder for use in future lab exercises:
1. `caesar_cipher.txt`
2. `vigenere_cipher.txt`
3. `frequency_analysis.txt`
4. `rsa_algorithm.txt`
5. `hash_functions.txt`

---

### Task 7: README Documentation

The `README.md` provides:
- Project title & course information (22CPP307).
- Team members table (Rishi - Roll No: 20241566).
- Complete directory structure description.
- How to run the application (`python main.py`).
- Semester module roadmap.

---

## 4. Git Commit History

To adhere to good software engineering standards, every task was committed separately with clean, professional commit messages:

| Hash | Type | Commit Message |
| :--- | :--- | :--- |
| `c27a70e` | `init:` | set up project structure with all required modules |
| `a703bd8` | `feat:` | add menu-driven CLI with encrypt, decrypt, attack, analyze options |
| `22234c7` | `feat:` | add file analysis with char, word, line count and letter frequency |
| `e802cd1` | `feat:` | add execution logger to record date, time and menu selection |
| `48df777` | `data:` | add five sample text files for cryptanalysis exercises |
| `58b6996` | `docs:` | add complete README with project info, structure and future modules |
| `1c441da` | `fix:` | use ASCII-safe characters for Windows terminal compatibility |
| `9ff22f1` | `docs:` | add team member details to README |

---

## 5. Viva Preparation & Flashcards

### Q1: What is the main goal of Week 1?
**Answer**: Establishing project structure, Git setup, CLI interface, file analysis, logging, and documentation foundation. No cryptographic ciphers are implemented yet.

### Q2: Why is `__init__.py` used in folders?
**Answer**: It signals to Python that the directory should be treated as an importable package, enabling modular imports.

### Q3: How does the file analyzer count letter frequency?
**Answer**: It filters out non-alphabetic characters, converts letters to lowercase, and utilizes Python's `collections.Counter` to calculate letter occurrences.

### Q4: Why do we open log files in `"a"` mode instead of `"w"` mode?
**Answer**: Mode `"a"` (append) adds new log lines to the end of the file without deleting existing history. Mode `"w"` (write) would overwrite and erase previous logs.

### Q5: How do you execute the project?
**Answer**: Run `python main.py` from the root directory of the repository.

---

## 6. How to Run the Code

```bash
# Clone the repository
git clone https://github.com/the-sage-00/Cryptography-LabX.git

# Move into the project directory
cd Cryptography-LabX

# Launch the interactive toolkit
python main.py
```
