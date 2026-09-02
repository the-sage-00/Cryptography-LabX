# CryptoLabX Assignment 1 — Complete Learning Guide

> This guide explains **everything** you did in Assignment 1, **why** you did it, and **what each part means**. Written in simple English so you can confidently explain it in your viva.

---

## What Is This Assignment About?

Your teacher wants you to build a **toolkit** (a collection of tools) called **CryptoLabX**. Think of it like a toolbox — right now the toolbox is empty, but over the semester you will fill it with cryptography tools (encryption, decryption, attacks, etc.).

**In Week 1**, you are only building the **empty toolbox** with proper labels on each drawer. No actual cryptography yet.

> **Real-world example**: Before a mechanic starts fixing cars, they first organize their workshop — set up shelves, label drawers, get a logbook. That's exactly what you're doing here.

---

## Why Do We Need All This?

| What | Why |
|------|-----|
| **Folder structure** | So your code is organized. Without it, all files would be in one messy folder. |
| **Git** | To track every change you make. If something breaks, you can go back in time. |
| **Menu (CLI)** | So users can interact with your toolkit easily. |
| **File analysis** | To practice reading files and counting things — a basic skill needed for cryptanalysis later. |
| **Logging** | To keep a record of what happened and when. Very important in real software. |
| **Datasets** | Sample text files you'll use later to test your ciphers and attacks. |
| **README** | Documentation — tells anyone looking at your project what it is and how to use it. |

---

## Task-by-Task Breakdown

---

### Task 1 & 2: Project Structure + Git Setup

#### What you did:
Created a GitHub repository and set up this folder structure:

```
CryptoLabX/
├── classical/       ← will hold Caesar cipher, Vigenere cipher, etc.
├── attacks/         ← will hold brute force attacks, frequency attacks, etc.
├── math/            ← will hold math functions (GCD, modular arithmetic)
├── modern/          ← will hold AES, RSA, DES, etc.
├── analysis/        ← holds file analysis tool (reading & counting text)
├── datasets/        ← holds sample text files
├── outputs/         ← holds log files and generated results
├── docs/            ← holds documentation
├── tests/           ← will hold test files
├── utils/           ← holds utility tools (menu, logger)
├── main.py          ← the starting point of the program
├── README.md        ← project description
└── requirements.txt ← lists what libraries you need
```

#### Why each folder exists:

| Folder | Purpose | Simple Example |
|--------|---------|----------------|
| `classical/` | Old-school ciphers | Like a folder labeled "History Notes" |
| `attacks/` | Ways to break ciphers | Like a folder labeled "Cheat Sheets" |
| `math/` | Math helper functions | Like a calculator app |
| `modern/` | New-age ciphers | Like a folder labeled "Advanced Notes" |
| `analysis/` | Tools to study text | Like a word counter |
| `datasets/` | Sample data to work with | Like practice papers |
| `outputs/` | Results and logs | Like your answer sheets |
| `docs/` | Written documentation | Like your lab manual |
| `tests/` | Code to test your code | Like self-check quizzes |
| `utils/` | Helper tools used everywhere | Like pen, ruler — common tools |

#### What is `__init__.py`?

Every folder that has `__init__.py` becomes a **Python package**. This means Python can import code from that folder.

```python
# Without __init__.py → Python says: "I don't know this folder"
# With __init__.py    → Python says: "OK, I can use code from here"
```

#### What is `.gitkeep`?

Git does not track empty folders. So we put a tiny file called `.gitkeep` inside empty folders just so Git remembers they exist.

#### What is `.gitignore`?

A file that tells Git: **"Don't track these files."**

```
__pycache__/    ← Python's temporary compiled files (messy, not needed)
*.log           ← Log files (generated at runtime, not source code)
venv/           ← Virtual environment (too big, each person creates their own)
```

---

### What is Git? (Basics)

Git is a **version control system**. It saves snapshots of your project at different points in time.

#### Key Git commands you used:

| Command | What it does | Simple Example |
|---------|-------------|----------------|
| `git init` | Start tracking a folder | "Start a new diary" |
| `git add .` | Select all changed files to save | "Pick up the pages to file" |
| `git commit -m "message"` | Save a snapshot with a note | "Put pages in folder with a label" |
| `git push` | Upload your snapshots to GitHub | "Send your diary to the cloud" |
| `git log --oneline` | See all past snapshots | "Read the table of contents" |

#### What is a commit message?

A short note explaining **what you changed**. Good messages follow a pattern:

```
init:  ← for setup/initialization
feat:  ← for new features
fix:   ← for bug fixes
docs:  ← for documentation changes
data:  ← for data files
```

**Examples from your project:**
```
init: set up project structure with all required modules
feat: add menu-driven CLI with encrypt, decrypt, attack, analyze options
feat: add file analysis with char, word, line count and letter frequency
feat: add execution logger to record date, time and menu selection
data: add five sample text files for cryptanalysis exercises
docs: add complete README with project info, structure and future modules
```

---

### Task 3: Menu-Driven CLI

#### What is CLI?
**CLI = Command-Line Interface.** It's a text-based way to use a program (no mouse, no buttons — just typing).

#### What you built:

When you run `python main.py`, you see:

```
==================================================
         MAIN MENU
==================================================
  [1] Encrypt
  [2] Decrypt
  [3] Attack
  [4] Analyze
  [5] Exit
==================================================

  Enter your choice (1-5):
```

- Options 1, 2, 3 show **"Coming Soon"** (not built yet)
- Option 4 opens the **file analyzer** (Task 4)
- Option 5 **exits** the program

#### How does the code work?

**File: `main.py`** — The entry point. It runs a loop:

```python
while running:           # Keep showing menu
    display_menu()       # Show the options
    choice = get_user_choice()  # Ask user to pick
    running = handle_choice(choice)  # Do something based on pick
```

**File: `utils/menu.py`** — Contains all the menu logic:

- `display_banner()` → Prints the cool ASCII art title
- `display_menu()` → Prints the 5 options
- `get_user_choice()` → Reads what user types
- `handle_choice()` → Decides what to do based on the number typed

#### Why separate files?

This is called **modular design**. Instead of putting everything in one file:

```
main.py (1000 lines) ← BAD: hard to read, hard to find things
```

You split it into focused files:

```
main.py (30 lines)        ← just the loop
utils/menu.py (70 lines)  ← menu stuff
utils/logger.py (30 lines) ← logging stuff
analysis/file_analyzer.py (90 lines) ← analysis stuff
```

> **Viva tip**: If asked "why modular?", say: "It makes code easier to read, test, and maintain. Each file has one job."

---

### Task 4: File Analysis

#### What it does:
1. Lists all `.txt` files in the `datasets/` folder
2. User picks one
3. Program reads the file and shows:
   - **Total characters** — how many letters, spaces, symbols
   - **Total words** — how many words
   - **Total lines** — how many lines
   - **Unique characters** — how many different characters appear
   - **Letter frequency** — how many times each letter (a-z) appears

#### Sample output:

```
==================================================
  FILE ANALYSIS: caesar_cipher.txt
==================================================
  Total Characters  : 771
  Total Words       : 131
  Total Lines       : 8
  Unique Characters : 42

  ----------------------------------------
  LETTER FREQUENCY
  ----------------------------------------
    a :   44  ##############################
    e :   81  ##############################
    i :   52  ##############################
    t :   52  ##############################
```

#### Why is this important for cryptography?

**Frequency analysis** is one of the oldest ways to break ciphers. In English:
- `e` is the most common letter
- `t`, `a`, `o`, `i`, `n` are also very common
- `z`, `q`, `x` are rare

If someone encrypts a message with a simple cipher, the most common letter in the encrypted text is probably `e`. This is how you crack codes!

#### Key Python concepts used:

```python
# Reading a file
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Counting words
words = content.split()     # split by spaces → list of words
len(words)                  # count the list

# Counting lines
lines = content.splitlines()  # split by newlines → list of lines

# Finding unique characters
unique = set(content)  # set removes duplicates automatically

# Counting letter frequency
from collections import Counter
letters = [ch.lower() for ch in content if ch.isalpha()]
freq = Counter(letters)  # {'e': 81, 'a': 44, ...}
```

---

### Task 5: Logging

#### What is logging?
Keeping a **diary** of what happened in your program.

#### What your logger does:
Every time someone selects a menu option, it writes a line to `outputs/cryptolabx.log`:

```
[2026-08-04 21:37:37] Selected: Analyze
[2026-08-04 21:38:32] Selected: Analyze
```

#### Why is logging important?

1. **Debugging** — If something breaks, you can check the log to see what happened before it broke.
2. **Auditing** — In security, you need to know who did what and when.
3. **History** — You can see usage patterns over time.

#### Key Python concepts used:

```python
from datetime import datetime

# Get current date and time
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# Result: "2026-08-04 21:37:37"

# Append to file (not overwrite!)
with open(LOG_FILE, "a", encoding="utf-8") as f:  # "a" = append mode
    f.write(f"[{timestamp}] Selected: {option_name}\n")
```

> **Important**: `"a"` mode adds to the end of file. `"w"` mode would erase everything and start fresh. We use `"a"` so we keep all past logs.

---

### Task 6: Sample Datasets

#### What you created:
Five text files in the `datasets/` folder:

| File | Topic | Why it's useful |
|------|-------|-----------------|
| `caesar_cipher.txt` | Explains Caesar cipher | Test material for Caesar cipher implementation |
| `vigenere_cipher.txt` | Explains Vigenere cipher | Test material for Vigenere cipher implementation |
| `frequency_analysis.txt` | Explains frequency analysis | Good for testing frequency counter |
| `rsa_algorithm.txt` | Explains RSA algorithm | Test material for modern crypto assignments |
| `hash_functions.txt` | Explains hash functions | Test material for hashing assignments |

These files will be used in **future weeks** to test your encryption, decryption, and attack tools.

---

### Task 7: README

#### What is a README?
The **first file** anyone reads when they open your project. It answers:
- What is this project?
- Who made it?
- How is the code organized?
- How do I run it?
- What's coming next?

#### Your README includes:

1. **Project title and description**
2. **Team members** (Rishi - 20241566 + teammate TBD)
3. **Folder structure** with explanation of each folder
4. **Current features** (Week 1)
5. **How to run** (`python main.py`)
6. **Future modules** table (what's coming in Weeks 2-6)

---

## Complete File Map

Here's every file in your project and what it does:

```
CryptoLabX/
├── main.py                    ← START HERE. Runs the menu loop.
├── utils/
│   ├── __init__.py            ← Makes utils/ a Python package
│   ├── menu.py                ← All menu display and choice handling
│   └── logger.py              ← Writes timestamped logs to file
├── analysis/
│   ├── __init__.py            ← Makes analysis/ a Python package
│   └── file_analyzer.py       ← Reads text files, counts stats, shows frequency
├── datasets/
│   ├── caesar_cipher.txt      ← Sample text about Caesar cipher
│   ├── vigenere_cipher.txt    ← Sample text about Vigenere cipher
│   ├── frequency_analysis.txt ← Sample text about frequency analysis
│   ├── rsa_algorithm.txt      ← Sample text about RSA
│   └── hash_functions.txt     ← Sample text about hash functions
├── outputs/
│   └── cryptolabx.log         ← Generated at runtime (not in Git)
├── classical/                 ← Empty for now (future weeks)
├── attacks/                   ← Empty for now (future weeks)
├── math/                      ← Empty for now (future weeks)
├── modern/                    ← Empty for now (future weeks)
├── docs/                      ← Empty for now
├── tests/                     ← Empty for now
├── .gitignore                 ← Tells Git what to ignore
├── README.md                  ← Project documentation
└── requirements.txt           ← Python dependencies (none yet)
```

---

## How the Program Flows

```
User runs: python main.py
        │
        ▼
   Show Banner (ASCII art)
        │
        ▼
   ┌─→ Show Menu (5 options)
   │        │
   │        ▼
   │   User types a number
   │        │
   │        ▼
   │   Log the choice ──→ writes to outputs/cryptolabx.log
   │        │
   │        ▼
   │   ┌────┴────────────────────┐
   │   │ 1,2,3 = "Coming Soon"  │
   │   │ 4 = File Analysis      │
   │   │ 5 = Exit program       │
   │   └────┬────────────────────┘
   │        │
   │   (if not Exit)
   └────────┘
```

---

## Viva Preparation — Common Questions

### Q: What is the purpose of this project?
**A:** To build a modular cryptanalysis toolkit that will grow over the semester. Week 1 sets up the project foundation — folder structure, CLI, file analysis, and logging.

### Q: Why did you use Git?
**A:** Git tracks every change with timestamps and messages. If something breaks, we can go back to a working version. It also lets team members work together without overwriting each other's code.

### Q: What does modular design mean?
**A:** Splitting code into separate files, each with one specific job. For example, `menu.py` handles only the menu, `logger.py` handles only logging. This makes code easier to read, test, and maintain.

### Q: How does the file analysis work?
**A:** We read a text file, then use Python's `split()` to count words, `splitlines()` to count lines, `set()` to find unique characters, and `Counter` from the collections module to count how often each letter appears.

### Q: Why is letter frequency important in cryptography?
**A:** In English, some letters (like 'e', 't', 'a') appear much more often than others. If you encrypt text with a simple cipher, the frequency pattern stays the same. A cryptanalyst can use this pattern to crack the cipher.

### Q: What does the logger do?
**A:** It records every menu selection with the exact date and time into a log file (`outputs/cryptolabx.log`). This creates an audit trail of all program usage.

### Q: What is `__init__.py`?
**A:** It tells Python that the folder is a package (a collection of modules). Without it, Python cannot import code from that folder using `from folder import module`.

### Q: Why use `requirements.txt`?
**A:** It lists all external libraries the project needs. Anyone can run `pip install -r requirements.txt` to install everything. Right now it's empty because we only use built-in Python modules.

### Q: How many commits did you make and why?
**A:** One commit per task, so the progress is clearly tracked:
1. Project structure setup
2. Menu-driven CLI
3. File analysis module
4. Execution logger
5. Sample dataset files
6. README documentation

---

## Key Python Concepts Used

| Concept | Where Used | What It Does |
|---------|-----------|--------------|
| `if __name__ == "__main__"` | main.py | Runs code only when file is executed directly, not when imported |
| `from X import Y` | main.py, menu.py | Brings specific functions from other files |
| `with open() as f` | file_analyzer.py, logger.py | Opens a file safely (auto-closes when done) |
| `f-strings` (f"...") | everywhere | Puts variables inside strings easily |
| `dict` (dictionary) | menu.py | Maps keys to values (1→Encrypt, 2→Decrypt) |
| `set()` | file_analyzer.py | Removes duplicates from a collection |
| `Counter()` | file_analyzer.py | Counts how many times each item appears |
| `os.path.join()` | file_analyzer.py, logger.py | Creates file paths that work on any OS |
| `datetime.now()` | logger.py | Gets the current date and time |
| `.strip()` | menu.py | Removes extra spaces from user input |

---

> **Remember**: This assignment is the foundation. Every future week will add real cryptography tools into the folders you created today. Think of it as building the house structure before adding furniture.
