# CryptoLabX

**Cryptography Laboratory Toolkit**  
Course: Cryptography Laboratory (22CPP307)

---

## About

CryptoLabX is a modular cryptanalysis framework developed as part of the Cryptography Laboratory course. The toolkit is designed to grow incrementally over the semester, starting from a solid project foundation and expanding into a complete suite of classical and modern cryptographic algorithms, attack strategies, and analysis tools.

---

## Team Members

| Name             | Role                  |
|------------------|-----------------------|
| Member 1         | Developer / Analyst   |
| Member 2         | Developer / Analyst   |

> _Update the table above with actual team member names and roles._

---

## Project Structure

```
CryptoLabX/
├── classical/          # Classical cipher implementations (Caesar, Vigenere, Playfair, etc.)
├── attacks/            # Cryptanalysis attack modules (brute force, frequency analysis, etc.)
├── math/               # Mathematical utilities (modular arithmetic, GCD, prime generation)
├── modern/             # Modern cipher implementations (AES, DES, RSA, etc.)
├── analysis/           # Text and frequency analysis tools
│   └── file_analyzer.py
├── datasets/           # Sample text files for testing and analysis
│   ├── caesar_cipher.txt
│   ├── vigenere_cipher.txt
│   ├── frequency_analysis.txt
│   ├── rsa_algorithm.txt
│   └── hash_functions.txt
├── outputs/            # Generated output files and logs
├── docs/               # Documentation and reports
├── tests/              # Unit tests
├── utils/              # Utility modules (menu, logger, helpers)
│   ├── menu.py
│   └── logger.py
├── main.py             # Entry point — run with: python main.py
├── README.md           # Project documentation
├── requirements.txt    # Python dependencies
└── .gitignore          # Git ignore rules
```

---

## Features (Week 1)

- **Menu-Driven CLI**: Interactive command-line interface with options for Encrypt, Decrypt, Attack, Analyze, and Exit.
- **File Analysis**: Reads a text file from `datasets/` and displays character count, word count, line count, unique characters, and letter frequency.
- **Execution Logging**: Every menu selection is recorded with date and time in `outputs/cryptolabx.log`.
- **Sample Datasets**: Five curated text files covering cryptography topics for future assignments.

---

## How to Run

```bash
# Clone the repository
git clone https://github.com/the-sage-00/Cryptography-LabX.git
cd Cryptography-LabX

# Run the toolkit
python main.py
```

No external dependencies are required for Week 1.

---

## Future Modules

| Week | Module            | Description                                          |
|------|-------------------|------------------------------------------------------|
| 2    | Classical Ciphers | Caesar, Vigenere, Playfair cipher implementations    |
| 3    | Attacks           | Brute force, frequency analysis, known-plaintext     |
| 4    | Math Utilities    | Modular arithmetic, GCD, prime number generation     |
| 5    | Modern Ciphers    | AES, DES, RSA implementations                       |
| 6    | Analysis Tools    | Advanced frequency analysis, pattern recognition     |

---

## License

This project is developed for academic purposes as part of the Cryptography Laboratory (22CPP307) course.
