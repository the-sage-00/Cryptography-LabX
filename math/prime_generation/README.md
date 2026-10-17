# Cryptographic Prime Generation Using Miller–Rabin

## Course: Cryptography Laboratory (22CPP307) | Group: 10
**Students:** Rishi Saini (2024UCP1566) &nbsp;|&nbsp; Nandini Verma (2024UCP1667)  
**Instructor:** Dr. Meenakshi Tripathi  
**Department:** Computer Science and Engineering, MNIT Jaipur

---

## 1. Objective

The objective of this laboratory assignment is to generate a cryptographically strong probable prime of **512-bit length** using the **Miller–Rabin primality test**.

### Core Requirements:
1. Generate random odd candidate integers of the assigned bit length (512 bits).
2. Apply the Miller–Rabin test using multiple bases ($k = 40$ independent rounds).
3. If a candidate fails, generate another candidate and repeat.
4. Verify that the final generated number has exactly the assigned bit length ($512$) and passes the primality test across specified bases and independent libraries.

---

## 2. Theoretical Foundation

### 2.1 Prime Number Theorem & Search Complexity
The Prime Number Theorem states that the number of primes less than $x$ is asymptotically $\pi(x) \approx \frac{x}{\ln x}$.  
Consequently, the probability that a randomly chosen $b$-bit integer is prime is:
$$P(\text{prime}) \approx \frac{1}{\ln(2^b)} = \frac{1}{b \cdot \ln 2}$$

For $b = 512$:
$$\ln(2^{512}) = 512 \times 0.693147 \approx 354.89$$
Because even numbers (except 2) cannot be prime, we only generate and test **odd integers**, halving the search space:
$$\text{Expected Candidates} \approx \frac{354.89}{2} \approx 177 \text{ candidates}$$

To accelerate search performance, our implementation uses a **trial-division pre-filter** against precomputed primes up to 1000. This eliminates approximately **85% of composite candidates in microseconds**, avoiding expensive 512-bit modular exponentiations.

---

### 2.2 The Miller–Rabin Primality Test Algorithm
For any candidate odd integer $n > 2$, write $n - 1$ in the form:
$$n - 1 = 2^s \cdot d \quad \text{where } d \text{ is odd and } s \ge 1$$

For a chosen base $a \in [2, n - 2]$:
1. Compute $x = a^d \pmod n$.
2. If $x \equiv 1 \pmod n$ or $x \equiv -1 \equiv n - 1 \pmod n$, $n$ passes this round.
3. Otherwise, square $x$ repeatedly up to $s - 1$ times:
   $$x \leftarrow x^2 \pmod n$$
   - If $x \equiv n - 1 \pmod n$, $n$ passes this round.
   - If $x \equiv 1 \pmod n$, $n$ is **definitely composite** (violates the square-root-of-1 lemma).
4. If the loop finishes without observing $n - 1$, $n$ is **definitely composite**.

### 2.3 Error Probability & Security Bound
By the Monier–Rabin theorem, for any odd composite $n$, at most $\frac{1}{4}$ of all possible bases $a$ can be false witnesses (strong pseudoprime bases).  
When running $k$ independent random bases:
$$P(\text{composite passes } k \text{ rounds}) \le 4^{-k} = 2^{-2k}$$

For $k = 40$ rounds:
$$P(\text{error}) \le 4^{-40} = 2^{-80} \approx 8.27 \times 10^{-25}$$
This error probability is cryptographically negligible and conforms to NIST FIPS 186-4 recommendations for cryptographic prime generation.

---

## 3. Directory Structure

```text
math/prime_generation/
├── src/
│   ├── __init__.py            # Package interface
│   ├── miller_rabin.py        # Decomposition, single-base, k-round, and base verification
│   ├── prime_generator.py     # 512-bit odd generation, small prime pre-filtering
│   └── main.py                # Interactive CLI and --auto execution driver
├── testcases/
│   └── test_prime_gen.py      # 13 unit tests (Carmichael numbers, bit bounds, PyCryptodome)
├── outputs/
│   ├── results_table.txt      # Formatted experimental parameters table
│   └── prime_512.txt          # Stored 512-bit prime (decimal & hex)
├── screenshots/               # Terminal execution captures
├── reports/                   # Official laboratory report PDF
└── README.md                  # Comprehensive documentation
```

---

## 4. Experimental Results

Execution of `python math/prime_generation/src/main.py --auto` produces the following experimental submission table:

| Parameter | Value |
|:---|:---|
| **Assigned bit length** | 512 |
| **Actual bit length of the candidate** | 512 bits (Exact match: $2^{511} \le n < 2^{512}$) |
| **Number of candidates tested** | ~186 candidates |
| **Number of Miller–Rabin rounds** | 40 rounds ($P(\text{error}) \le 2^{-80}$) |
| **Total execution time** | ~0.058 seconds (58.17 ms) |
| **Specified bases passed** | 12/12 bases ($a \in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]$) |
| **Independent library verification** | PyCryptodome `isPrime()`: **CONFIRMED PRIME** |

---

## 5. Verification Demonstration

### 5.1 Bit-Length Verification
The candidate integer $n$ is constructed by:
```python
candidate = secrets.randbits(512)
candidate |= (1 << 511)  # Force MSB = 1
candidate |= 1          # Force LSB = 1
```
- Minimum possible value: $2^{511} + 1$ (bit length = 512)
- Maximum possible value: $2^{512} - 1$ (bit length = 512)
- Assertion: `assert prime.bit_length() == 512` **PASSED**.

### 5.2 Multi-Base Verification (12 Specified Bases)
The generated 512-bit prime was evaluated against 12 small prime bases:
$$a \in \{2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37\}$$
Each base satisfied either $a^d \equiv 1 \pmod n$ or $a^{d \cdot 2^r} \equiv -1 \pmod n$, confirming zero composite witness contradictions across all 12 bases.

### 5.3 Independent Library Verification
The generated number was cross-verified using `Crypto.Util.number.isPrime()` from the trusted `pycryptodome` library:
- **Result:** `True` (Independent Confirmation).

---

## 6. How to Run

### Automated Execution (Table & Verification)
```powershell
python math/prime_generation/src/main.py --auto
```

### Interactive CLI Menu
```powershell
python math/prime_generation/src/main.py
```

### Unit Test Suite
```powershell
python math/prime_generation/testcases/test_prime_gen.py
```
