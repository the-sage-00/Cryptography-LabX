<div align="center">

<img src="READMEtopheadimage.jpeg" alt="Malaviya National Institute of Technology Jaipur" width="100%">

# CryptoLabX

### Cryptography Laboratory Toolkit & Semester-Long Security Project
**Department of Computer Science and Engineering**  
**Malaviya National Institute of Technology Jaipur**

---

</div>

## Laboratory Information & Metadata

| Field | Detail |
|:---|:---|
| **Course** | Cryptography Laboratory (22CPP307) |
| **Department** | Department of Computer Science and Engineering, MNIT Jaipur |
| **Course Instructor / Professor** | Course Faculty / Lab Incharge |
| **Team Members** | **1. Rishi Saini** (2024UCP1566)<br>**2. Nandini Verma** (2024UCP1667) |
| **Group Number** | Group 10 (Even Group Number) |
| **Assigned Application** | IoT Device Management System |
| **Programming Language** | Python 3.11+, C++ (ISO C++11) |
| **SAST Tool** | Semgrep (Static Application Security Testing) |

---

## Lab Progress Checklist

- [x] **Lab 1: Project Setup, Repository Structure & Modular CLI**
  - Modular directory architecture adhering to course guidelines.
  - Interactive CLI menu with execution logging to `outputs/cryptolabx.log`.
  - Frequency and corpus analysis utilities in `analysis/file_analyzer.py`.
  - Five curated cryptanalysis datasets in `datasets/`.

- [x] **Lab 2: Classical Ciphers Implementation**
  - Shift Cipher, Caesar Cipher, and polyalphabetic foundation modules.

- [x] **Lab 3: Secure Application (IoT Device Management) & SAST Analysis**
  - Core IoT device management: device registration, status monitoring, firmware uploads.
  - Identification and remediation of vulnerabilities: Command Injection, Path Traversal, SQL Injection.
  - Automated SAST scan automation via Semgrep with structured JSON/text reports in `secure_application/reports/`.
  - Automated unit test suite with 100% passing rate in `secure_application/testcases/`.

- [x] **Lab 4: Cryptanalysis of Shift Cipher**
  - Key space exploration (26 keys).
  - Automated brute-force attack combined with English dictionary lookup scoring.
  - Statistical Chi-Square ($\chi^2$) goodness-of-fit cryptanalysis.
  - Automated evaluation across 5 test cases and comparative summary report.

- [x] **Lab 5: Cryptanalysis of Monoalphabetic Substitution Cipher**
  - C++ cryptanalytic engine for large key space ($26! \approx 4.03 \times 10^{26}$).
  - Six mandatory cryptanalytic functions: `frequency_analysis()`, `word_frequency_analysis()`, `pattern_analysis()`, `apply_substitution()`, `display_partial_plaintext()`, and `verify_solution()`.
  - Pattern signature recognition (e.g., 0.1.2.0 for `THAT`).
  - 100% plaintext recovery benchmarked against ground truth (Katz & Lindell, p. 40).

- [x] **Lab 6: Cryptanalysis of Vigenère Cipher (Group 10 Assignment)**
  - Assigned Dataset: Ciphertext-2 (Even Group Numbers, 758 letters).
  - Automated Kasiski examination: repeated 3-gram to 5-gram distance factor ranking.
  - Index of Coincidence (IC) evaluation: confirming key length $L = 12$ ($IC = 0.0717$ matching English).
  - Coset partitioning into 12 streams and individual Caesar shift derivation via Chi-Square minimization.
  - Recovered Key: `UNITEDSTATES`.
  - 100% exact character match verification via re-encryption.

- [x] **Lab 7: Padding Oracle Attack on AES-CBC (Keyless Plaintext Recovery)**
  - Demonstration of keyless plaintext recovery against AES-CBC using only PKCS#7 padding oracle feedback.
  - Zero AES key access: secret key is never exported or accessed by the attack algorithm.
  - Right-to-left byte recovery algorithm with disambiguation logic for single-byte padding (`0x01`).
  - Analysis of query complexity: theoretical worst-case ($256 \times 16 \times N$) vs. average ($128 \times 16 \times N$) vs. measured queries (~50% efficiency gain).
  - Prevention recommendations: Authenticated Encryption (AES-GCM), Encrypt-then-MAC (HMAC-SHA256), and TLS 1.3 protocol standards.
  - 17 unit tests passing across single-block, multi-block, and edge-case inputs.

---

## Repository Structure

```text
CryptoLabX/
├── READMEtopheadimage.jpeg             # MNIT Jaipur campus header image
├── classical/                          # Classical cipher implementations
│   └── __init__.py
├── modern/                             # Modern block and public key ciphers
│   └── __init__.py
├── hashing/                            # Cryptographic hashing modules (SHA-256, HMAC)
│   └── __init__.py
├── attacks/                            # Cryptanalysis attack modules
│   ├── shift_cipher_attack/            # Assignment 4: Shift Cipher Cryptanalysis
│   │   ├── src/                        # Python attack scripts (brute force, chi-square)
│   │   ├── dictionary/                 # English word validation list
│   │   ├── outputs/                    # Results table
│   │   ├── reports/                    # Assignment 4 PDF Report
│   │   ├── screenshots/                # Terminal execution captures
│   │   ├── testcases/                  # Test case definitions
│   │   └── README.md
│   ├── mono_substitution_attack/       # Assignment 5: Monoalphabetic Cipher Attack
│   │   ├── src/                        # C++ source code (mono_cipher.cpp)
│   │   ├── plaintext/                  # Source text (Katz & Lindell, Page 40)
│   │   ├── outputs/                    # Generated ciphertext
│   │   ├── reports/                    # Assignment 5 PDF Report
│   │   ├── screenshots/                # Terminal execution captures
│   │   └── README.md
│   ├── vigenere_cipher_attack/         # Assignment 6: Vigenère Cipher Cryptanalysis
│   │   ├── src/                        # Python cryptanalysis driver and modules
│   │   ├── outputs/                    # Detailed experimental results table
│   │   ├── reports/                    # Assignment 6 PDF Report
│   │   ├── screenshots/                # Terminal execution captures
│   │   ├── testcases/                  # Group ciphertexts (Even & Odd)
│   │   └── README.md
│   ├── padding_oracle_attack/          # Assignment 7: Padding Oracle Attack on AES-CBC
│   │   ├── src/                        # AES-CBC oracle and right-to-left attack engine
│   │   ├── outputs/                    # Recovered plaintext and query records
│   │   ├── reports/                    # Assignment 7 PDF Report
│   │   ├── screenshots/                # Terminal execution captures
│   │   ├── testcases/                  # Predefined scenarios and test suite (17 tests)
│   │   └── README.md
│   └── __init__.py
├── analysis/                           # Text and corpus analysis tools
│   ├── file_analyzer.py
│   └── __init__.py
├── secure_application/                 # Assignment 3: Semester Long Project Application
│   ├── src/                            # IoT Device Management System
│   ├── sast/                           # Semgrep SAST scan automation scripts
│   ├── reports/                        # Semgrep scan reports (JSON and TXT)
│   ├── screenshots/                    # Application and SAST scan screenshots
│   ├── crypto/                         # Security utility & crypto helper layer
│   │   └── __init__.py
│   ├── outputs/                        # Application logs and runtime output
│   ├── testcases/                      # Unit test suite for IoT Manager
│   └── README.md
├── datasets/                           # Curated sample texts for testing and analysis
├── docs/                               # Lab manuals and theoretical documentation
│   ├── assignments/                    # Course assignment instruction manuals
│   └── learning_guide.md
├── outputs/                            # Framework logs (cryptolabx.log)
├── tests/                              # Global framework unit tests
├── utils/                              # CLI menu, logger, and shared helpers
├── main.py                             # Main CLI entry point
├── requirements.txt                    # Project Python dependencies
├── .gitignore                          # Standard git ignore rules
└── README.md                           # Master repository documentation
```

---

## Execution Instructions

### Prerequisites & Installation

```powershell
# Clone the repository
git clone https://github.com/the-sage-00/Cryptography-LabX.git
cd Cryptography-LabX

# Install Python dependencies
pip install -r requirements.txt
```

---

### Running Individual Assignments

#### 1. Framework CLI & Text Analyzer (Lab 1)
```powershell
python main.py
```

#### 2. Secure Application & SAST Security Scan (Lab 3)
```powershell
# Run IoT Device Management Application
python secure_application/src/iot_device_manager.py

# Run Semgrep SAST Scan
python secure_application/sast/run_scan.py

# Run Unit Tests
python secure_application/testcases/test_iot_manager.py
```

#### 3. Shift Cipher Cryptanalysis (Lab 4)
```powershell
# Automated evaluation across all test cases
python attacks/shift_cipher_attack/src/main.py

# Run test suite
python attacks/shift_cipher_attack/testcases/test_cases.json
```

#### 4. Monoalphabetic Substitution Cipher (Lab 5)
```powershell
# Compile C++ engine
g++ -o attacks/mono_substitution_attack/src/mono_cipher.exe attacks/mono_substitution_attack/src/mono_cipher.cpp -std=c++11

# Run interactive cryptanalysis
cd attacks/mono_substitution_attack
.\src\mono_cipher.exe
```

#### 5. Vigenère Cipher Cryptanalysis (Lab 6 - Group 10 Dataset)
```powershell
# Automated execution (Kasiski + IC + Coset Chi-Square + Decryption + Verification)
python attacks/vigenere_cipher_attack/src/main.py --auto

# Interactive menu
python attacks/vigenere_cipher_attack/src/main.py
```

#### 6. Padding Oracle Attack on AES-CBC (Lab 7)
```powershell
# Automated demonstration on all test scenarios
python attacks/padding_oracle_attack/src/main.py --auto

# Interactive attack menu
python attacks/padding_oracle_attack/src/main.py

# Run full unit test suite (17 tests)
python attacks/padding_oracle_attack/testcases/test_padding_oracle.py
```

---

## Academic Integrity & Version Control

- All implementations in this repository were independently developed by **Group 10** members.
- Commits are maintained incrementally and descriptively to document the architectural evolution of the toolkit throughout the semester.
