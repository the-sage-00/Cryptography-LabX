# Cryptography Laboratory (22CPP307) - Assignment Questions (Group 10)

Compiled from the assignment sheets. Group 10 = even group number; application no. 10; textbook page 10 + 30 = **40**.

---
## General Laboratory Guidelines
* **One** GitHub repository for the whole semester, named `CryptoLabX_GroupNumber_Name1_Name2`; no new repository per experiment.
* Required layout: `classical/ modern/ hashing/ attacks/ analysis/ docs/ secure_application/{src,reports,screenshots,sast,crypto,outputs,testcases,README.md} README.md .gitignore`.
* **Git:** at least two meaningful commits per laboratory with descriptive messages (e.g. "Created Login Module", "Generated Semgrep Report"). Avoid "Final", "Update", "Done", "Lab Complete".
* **README.md** must list student names, roll numbers, assigned application, programming language, SAST tool and a lab progress checklist.
* **Handwritten notebook** per experiment: Aim, brief theory (5-10 lines), algorithm/flowchart, important commands, observations. Do not copy complete source code.
* **Every lab:** perform the experiment → commit to GitHub → update README → update notebook → upload nothing to Google Drive.
* **Submission:** Mid-term - repository (commits, code, README), notebook, viva. End-term - final repository, notebook, viva.
* **Academic integrity:** own work as the assigned group; copying code/repositories/online sources is not permitted; be ready to explain implementation, Git history and security decisions.

---
## Assignment 1 (Week 1): Build Your CryptoLabX Toolkit
Create the toolkit foundation only - **no cryptographic algorithms**.
Structure: `classical/ attacks/ math/ modern/ analysis/ datasets/ outputs/ docs/ tests/ utils/ main.py README.md requirements.txt`.

1. Create a Git repository `CryptoLabX_GroupXX`, initialise Git, first commit with the project structure.
2. Create the folder structure.
3. Menu-driven CLI with options Encrypt, Decrypt, Attack, Analyze, Exit (options may display "Coming Soon").
4. Read a text file from `datasets/` and display number of characters, words, lines, unique characters and letter frequency.
5. Maintain a log file recording date, time and selected menu option for every execution.
6. `datasets/` with at least five text files.
7. README: project, team members, folder structure, future modules.

**Deliverables:** GitHub URL, source code, screenshot of project structure, screenshot of working menu, sample file-analysis output, generated log file, README (1-2 pages). Individual viva.

---
## Lab Assignment 3: Secure Application and SAST
Each group develops one small console (or Java GUI) application with the given functionalities and **3 vulnerabilities**, chosen by (group number % 10). Language follows the installed SAST tool.

| No. | Application | Suggested vulnerabilities (any 3) |
|---|---|---|
| 1 | ATM System | Hardcoded credentials, improper input validation, SQL injection, missing authentication checks, information leakage via errors |
| 2 | Online Banking | SQL injection, broken access control, insecure session management, insufficient input validation, sensitive data in logs |
| 3 | Hospital Management | SQL injection, broken access control, file upload, missing authorization, path traversal |
| 4 | Library Management | SQL injection, XSS, improper input validation, directory traversal, missing authentication |
| 5 | Drone Control | Command injection, missing authentication, buffer overflow (C), improper input validation, insecure file handling |
| 6 | Cryptocurrency Wallet | Broken access control, insecure session handling, input validation errors, hardcoded secrets, information leakage |
| 7 | Student Portal | SQL injection, XSS, broken access control, IDOR, missing authorization |
| 8 | E-Commerce | SQL injection, XSS, IDOR, file upload, price manipulation |
| 9 | Password Manager | Hardcoded credentials, missing authentication, information leakage, improper file permissions, insecure storage |
| **10** | **IoT Device Management** | **Command injection, path traversal, missing authentication, insecure file upload, improper input validation** |

Core functionalities for application 10: smart device registration, status monitoring, firmware upload, configuration management.
Continue in the same repository; create `secure_application/` (`src, reports, screenshots, sast, outputs, testcases, README.md`). Do not change the assigned application.

---
## Assignment 4: Cryptanalysis of Shift Cipher (Brute Force, Dictionary Scoring, Chi-Square)
**Notebook:** (1) both cryptanalysis algorithms, (2) comparison of the dictionary-scoring key and the Chi-Square key, (3) failure analysis with improvement, (4) observations from your own results, (5) conclusion. Keep a results table: *Test Case | Actual Key | Dictionary Key | Chi-Square Key | Dictionary Correct? | Chi-Square Correct?*
**Repository:** `attacks/shift_cipher_attack/{src/{shift_cipher.py,brute_force_dictionary.py,chi_square_attack.py,main.py},dictionary/english_words.txt,testcases/,outputs/,screenshots/,reports/Assignment_4_Report.pdf,README.md}`
**Commits:** 1 Implemented Shift Cipher; 2 Added brute-force and dictionary scoring; 3 Added Chi-Square cryptanalysis; more for testing, bug fixing, documentation.

---
## Assignment 5: Monoalphabetic Substitution Cipher - Frequency and Pattern Analysis (any language)
Implement the cipher and generate ciphertext. Plaintext (≥ 1 page) from *Modern Cryptography* (Katz & Lindell), page **Group_number + 30**.
* Letter-frequency analysis: count each ciphertext letter, list in descending order, percentage per letter, identify the most frequent letters.
* Use word patterns and repeated words: one-letter, two-letter, three-letter words, repeated words, repeated letter patterns.
* Iteratively recover the plaintext (no library function): propose candidate substitutions, replace suspected letters, examine partial plaintext, reject incorrect hypotheses, continue until meaningful.
* Recover the substitution key and validate it by re-encrypting the plaintext.
* Document and justify decisions in the notebook table: *Step | Observation | Possible Substitution | Substitution Tested | Result | Decision*.
* Required functions: `frequency_analysis()`, `word_frequency_analysis()`, `pattern_analysis()`, `apply_substitution()`, `display_partial_plaintext()`, `verify_solution()`.
Write the algorithm in the notebook and add the code to the repository.

---
## Assignment 6: Cryptanalysis of Vigenère Cipher (Kasiski Examination and Frequency Analysis)
The program must: preprocess the ciphertext (given per group number); estimate key length with Kasiski; split into groups; frequency analysis per group; determine the probable key; decrypt; **display** estimated key length, frequency table for each group, recovered key, recovered plaintext; verify by re-encrypting.
Required functions: `clean_ciphertext, find_repeated_patterns, calculate_distances, find_factors, kasiski_analysis, calculate_ic, split_into_groups, frequency_analysis, find_shift, find_key, vigenere_decrypt, vigenere_encrypt, verify`.
Ciphertext 1 (odd groups) and Ciphertext 2 (even groups) are given on the sheet; **group 10 uses Ciphertext 2** (758 letters). Both are stored in `attacks/vigenere_cipher_attack/testcases/ciphertexts.json`.

---
## Assignment 7: Padding Oracle Attack
Recover plaintext from AES-CBC without the key, given the ciphertext, IV, a padding-oracle function (valid PKCS#7 padding?) and starter code.
1. Explain AES-CBC, PKCS#7 padding and the role of a padding oracle.
2. Implement the attack: modify the previous ciphertext block, query the oracle, recover bytes right to left, recover the complete plaintext.
3. Record the total number of oracle queries and explain why modifying the previous block affects the target block's plaintext.
4. Explain how to prevent the vulnerability in a real system.
**Constraints:** the AES key must not be used during the attack; no ready-made padding-oracle library; not hard-coded to one plaintext.
**Deliverables:** Python program, recovered plaintext, number of oracle queries, brief explanation of attack and prevention.

---
## Assignment 8: Cryptographic Prime Generation Using Miller-Rabin
Generate a probable prime of **512 bits**: random odd candidates → Miller-Rabin with multiple bases → regenerate on failure → verify exact bit length and primality.
**Submit** a table (Assigned bit length, Generated prime candidate, Actual bit length, Number of candidates tested, Number of Miller-Rabin rounds, Total execution time) and a **verification**: exact bit length, passes Miller-Rabin for the specified bases, confirmed by an independent method or trusted library.
