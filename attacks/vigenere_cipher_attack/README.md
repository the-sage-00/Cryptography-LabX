# Cryptanalysis of Vigenère Cipher using Kasiski Examination and Frequency Analysis

## Course: Cryptography Laboratory (22CPP307) | Group: 10 (Even Group Number)

---

## 1. Purpose
The objective of this laboratory assignment is to perform automated and theoretical cryptanalysis on a polyalphabetic Vigenère ciphertext without prior knowledge of the encryption key or key length. The attack operates through:
1. **Kasiski Examination:** Identifying repeated sequences (trigrams to 5-grams), calculating distance intervals, and evaluating common factors.
2. **Index of Coincidence (IC):** Statistical analysis to confirm candidate key lengths (English monogram IC $\approx 0.068$ vs. random polyalphabetic IC $\approx 0.038$).
3. **Coset Partitioning & Caesar Frequency Analysis:** Splitting ciphertext into $L$ independent cosets and estimating each key character via Chi-Square goodness-of-fit.
4. **Key Reconstruction & Decryption:** Assembling the probable key string and recovering full plaintext.
5. **Re-encryption Verification:** Encrypting the recovered plaintext with the derived key and confirming exact character match against the original ciphertext.

---

## 2. Target Dataset (Group 10 Assignment)
As specified by the laboratory guidelines, **Group 10** corresponds to an **Even Group Number**, assigned **Ciphertext-2**:

* **Assigned Dataset:** Ciphertext-2 (Even Group Numbers)
* **Ciphertext Length:** 758 uppercase letters (normalized)
* **Estimated Key Length ($L$):** 12
* **Recovered Key:** `UNITEDSTATES`
* **Plaintext Source:** United States Declaration of Independence (Closing Resolution)
* **Re-encryption Verification:** 100% Exact Match

---

## 3. Required User-Defined Functions Implemented

| # | Function | Purpose |
|---|:---|:---|
| 1 | `clean_ciphertext()` | Removes whitespaces/non-alphabetic characters and normalizes ciphertext to uppercase A-Z |
| 2 | `find_repeated_patterns()` | Identifies repeated sequences (length 3 to 5) and records all occurrence positions |
| 3 | `calculate_distances()` | Computes distances between consecutive occurrences of repeated patterns |
| 4 | `find_factors()` | Finds common factors of distances to identify candidate key lengths |
| 5 | `kasiski_analysis()` | Ranks candidate key lengths by factor frequency counts |
| 6 | `calculate_ic()` | Calculates Index of Coincidence ($IC = \frac{\sum f_i(f_i-1)}{N(N-1)}$) |
| 7 | `split_into_groups()` | Divides ciphertext into $L$ independent cosets corresponding to key length |
| 8 | `frequency_analysis()` | Calculates unigram A–Z frequency distribution for each group |
| 9 | `find_shift()` | Estimates individual Caesar shift for each group using Chi-Square minimization |
| 10 | `find_key()` | Combines shifts from all cosets into the probable Vigenère key |
| 11 | `vigenere_decrypt()` | Decrypts ciphertext using recovered key ($P_i = (C_i - K_{i \pmod L}) \pmod{26}$) |
| 12 | `vigenere_encrypt()` | Re-encrypts plaintext for verification ($C_i = (P_i + K_{i \pmod L}) \pmod{26}$) |
| 13 | `verify()` | Verifies that re-encrypted text exactly matches original normalized ciphertext |

---

## 4. Execution Instructions

### Run Automated Evaluation (Group 10 Dataset):
```powershell
python attacks/vigenere_cipher_attack/src/main.py --auto
```

### Run Interactive Menu:
```powershell
python attacks/vigenere_cipher_attack/src/main.py
```

Menu options include:
- `[1]` Run Cryptanalysis on Group 10 Dataset (Ciphertext-2, Even)
- `[2]` Run Cryptanalysis on Ciphertext-1 (Odd Group Numbers)
- `[3]` Inspect Detailed A-Z Frequency Table for a Specific Group
- `[4]` Custom Ciphertext Cryptanalysis
- `[5]` Exit

---

## 5. Experimental Results Summary (Group 10)

### Kasiski & IC Key Length Confirmation:
* **Kasiski Factor Peaks:** Lengths 2, 3, 4, 6, 12 (all factors of 12).
* **Average IC Peak:** Length 12 gives $IC = 0.0717$ (closest match to English $0.068$).

### Recovered Key Characters by Coset:
| Coset | Size | Shift ($k_i$) | Key Letter | Min $\chi^2$ Score |
|:---:|:---:|:---:|:---:|:---:|
| 1 | 64 | 20 | **U** | 14.32 |
| 2 | 64 | 13 | **N** | 21.86 |
| 3 | 63 | 8 | **I** | 22.39 |
| 4 | 63 | 19 | **T** | 34.12 |
| 5 | 63 | 4 | **E** | 19.88 |
| 6 | 63 | 3 | **D** | 30.49 |
| 7 | 63 | 18 | **S** | 28.29 |
| 8 | 63 | 19 | **T** | 22.52 |
| 9 | 63 | 0 | **A** | 13.25 |
| 10 | 63 | 19 | **T** | 19.90 |
| 11 | 63 | 4 | **E** | 19.63 |
| 12 | 63 | 18 | **S** | 24.04 |

**Reconstructed Key:** `UNITEDSTATES`  
**Re-encryption Test:** `YES [100% MATCH]`
