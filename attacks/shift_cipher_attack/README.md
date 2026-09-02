# CryptoLabX — Shift Cipher Cryptanalysis (Assignment 4)

**Course**: Cryptography Laboratory (22CPP307)  
**Module**: `attacks/shift_cipher_attack`

---

## 📌 1. Laboratory Purpose

The purpose of this lab is to perform automated cryptanalysis on the Shift Cipher (Caesar Cipher) using two distinct analytical methods:
1. **Exhaustive Brute-Force with Dictionary Scoring**
2. **Chi-Square ($\chi^2$) Goodness-of-Fit Letter Frequency Analysis**

The goal is to evaluate the key prediction accuracy, limitations, failure conditions, and comparative advantages of each method across different text characteristics (length, presence of spaces, non-standard letter distributions).

---

## 📐 2. Cryptanalysis Algorithms

### A. Brute-Force & Dictionary Scoring Algorithm

The Shift Cipher has a key space of size $|K| = 26$. For every key $k \in \{0, 1, \dots, 25\}$:

1. Decrypt ciphertext: $P_{\text{candidate}} = (C - k) \pmod{26}$.
2. Tokenize $P_{\text{candidate}}$ into words using regular expressions (`[a-zA-Z]+`).
3. Compare extracted words against an English word dictionary (`english_words.txt`).
4. Calculate match count $M$ and match percentage:
   $$\text{Score} = \left( \frac{\text{Matched Words}}{\text{Total Tokenized Words}} \right) \times 100\%$$
5. Select the key $k$ that maximizes the dictionary match score as the predicted key.

```
Input: Ciphertext C, Dictionary D
For k = 0 to 25:
    P = Decrypt(C, k)
    Words = Tokenize(P)
    Score[k] = Count(w in D for w in Words)
Predicted Key = argmax(Score)
```

---

### B. Chi-Square ($\chi^2$) Letter Frequency Analysis Algorithm

Chi-Square analysis evaluates how closely letter frequencies in decrypted candidate text match standard English monograph probabilities ($P_A \approx 0.08167, P_E \approx 0.12702$, etc.).

For each candidate decryption $P_{\text{candidate}}$ with total alphabetic characters $N$:
1. Count observed frequency $O_i$ for each letter $i \in \{'A', 'B', \dots, 'Z'\}$.
2. Compute expected frequency: $E_i = N \times P_i$.
3. Compute Chi-Square statistic:
   $$\chi^2 = \sum_{i='A'}^{'Z'} \frac{(O_i - E_i)^2}{E_i}$$
4. The key $k$ yielding the **minimum $\chi^2$ score** corresponds to the closest statistical match to English and is chosen as the predicted key.

```
Input: Ciphertext C, English Monogram Probabilities P
For k = 0 to 25:
    P_cand = Decrypt(C, k)
    N = CountAlphabeticLetters(P_cand)
    chi_sq[k] = Sum( (O_i - N*P_i)^2 / (N*P_i) for i in A..Z )
Predicted Key = argmin(chi_sq)
```

---

## 📊 3. Experimental Results Table

| Test Case # | Description | Actual Key | Dictionary Key | Chi-Square Key | Dictionary Correct? | Chi-Square Correct? |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **1** | Standard Medium Text with Spaces | **7** | **7** | **7** | **YES** | **YES** |
| **2** | Long Technical English Text | **15** | **15** | **15** | **YES** | **YES** |
| **3** | Short English Text (3 words) | **3** | **3** | **3** | **YES** | **YES** |
| **4** | Continuous Text Without Spaces | **12** | **0** | **12** | **NO** | **YES** |
| **5** | High Z/J Rare Letter Text | **19** | **19** | **25** | **YES** | **NO** |

---

## ⚖️ 4. Comparison of Cryptanalysis Methods

| Feature | Dictionary Scoring Attack | Chi-Square ($\chi^2$) Analysis Attack |
| :--- | :--- | :--- |
| **Primary Mechanism** | Word matching against English dictionary | Statistical goodness-of-fit against letter frequencies |
| **Dependency on Spaces** | **High** — Tokenizer relies on spaces | **Zero** — Operates on raw letter distributions |
| **Short Text Accuracy** | **High** (if words are standard) | **Moderate** (needs $\ge 30-50$ letters for accuracy) |
| **Rare Letter Handling** | **Robust** (words like "JAZZ" scored correctly) | **Sensitive** to high occurrences of rare letters ('Z', 'J') |
| **Computational Speed** | Fast ($O(26 \cdot W)$ where $W$ = word count) | Extremely Fast ($O(26 \cdot N)$ letter ops) |

---

## 🔍 5. Failure Analysis & Recommended Improvements

### 1. Failure Mode in Test Case 4 (Dictionary Attack Failed: Key 0 vs 12)
- **Why it failed**: The input text `DEFENDTHEEASTWALLOFTHECASTLEATDAWN` contains no space separators. The regex tokenizer treats the entire 34-character string as a single candidate word. Since `DEFENDTHEEASTWALLOFTHECASTLEATDAWN` is not in `english_words.txt`, dictionary score remains 0 for all keys, resulting in a default tie-break key of 0.
- **Suggested Improvement**: Implement **string segmentation (word splitting)** algorithms (e.g., dynamic programming using dictionary unigrams) or **character $n$-gram language modeling** (bigram/trigram probability scoring).

### 2. Failure Mode in Test Case 5 (Chi-Square Attack Failed: Key 25 vs 19)
- **Why it failed**: Text `JAZZ RHYTHM BUZZ QUIZ VEX` (Key 19) contains a high density of rare English letters ('Z', 'J', 'Q', 'X'). The observed frequencies deviate heavily from standard English letter expectations ($P_Z = 0.00074$), inflating the $\chi^2$ error value. Candidate shift 25 coincidentally produces a lower $\chi^2$ score.
- **Suggested Improvement**: Combine Chi-Square evaluation with Dictionary Scoring in a **hybrid voting system** (Weighted Score = $\alpha \cdot \text{DictScore} + \beta \cdot \frac{1}{\chi^2}$).

---

## 💡 6. Observations & Conclusion

### Observations:
1. **Letter Frequency Efficiency**: Chi-Square analysis is completely invariant to word boundaries and spaces, making it superior for continuous or encrypted texts without punctuation.
2. **Text Length Threshold**: Chi-Square accuracy improves dramatically as text length exceeds 50 characters, approaching $100\%$ reliability.
3. **Dictionary Resilience**: Dictionary scoring is highly effective for short texts as long as space delimiters are intact.

### Conclusion:
The Shift Cipher offers **zero effective security** against modern cryptanalysis. With a tiny key space $|K| = 26$, exhaustive key recovery takes less than $1$ millisecond. Using either Dictionary Scoring or Chi-Square Analysis (or a hybrid combination), the secret key and plaintext can be reliably recovered without key knowledge.

---

## 📂 Repository Structure

```text
attacks/shift_cipher_attack/
├── src/
│   ├── shift_cipher.py           # Shift cipher encryption/decryption
│   ├── brute_force_dictionary.py # Dictionary scoring cryptanalysis
│   ├── chi_square_attack.py      # Chi-Square frequency analysis
│   ├── main.py                   # Automated test driver & CLI
│   └── __init__.py               # Package initializer
├── dictionary/
│   └── english_words.txt         # English word dictionary list
├── testcases/
│   └── test_cases.json           # Predefined test suite
├── outputs/
│   └── results_table.txt         # Generated results table & report
├── screenshots/                  # Execution screenshots placeholder
├── reports/
│   └── Assignment_4_Report.pdf   # Generated PDF Lab Report
└── README.md                     # Lab notebook & documentation
```

---

## 🚀 How to Run

```bash
# Run automated test suite & generate results table
python attacks/shift_cipher_attack/src/main.py --auto

# Interactive CLI menu (custom text testing)
python attacks/shift_cipher_attack/src/main.py

# Re-generate PDF Report
python attacks/shift_cipher_attack/reports/generate_pdf.py
```
