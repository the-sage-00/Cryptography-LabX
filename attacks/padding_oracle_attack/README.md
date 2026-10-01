# Padding Oracle Attack on AES-CBC

## Course: Cryptography Laboratory (22CPP307) | Group: 10 (Even Group Number)

---

## 1. Purpose

The objective of this laboratory assignment is to demonstrate how a **Padding Oracle Attack** can recover the complete AES-CBC plaintext from a ciphertext **without knowing the encryption key**, using only a boolean oracle that answers:

> *"Does the decrypted ciphertext have valid PKCS#7 padding?"*

---

## 2. Task 1 — Understanding the Attack

### AES-CBC (Cipher Block Chaining)

| Operation   | Formula |
|:---:|:---|
| Encryption  | $C_i = \text{AES\_ENC}(P_i \oplus C_{i-1}),\quad C_0 = \text{IV}$ |
| Decryption  | $P_i = \text{AES\_DEC}(C_i) \oplus C_{i-1},\quad C_0 = \text{IV}$ |

Each plaintext block is XOR-ed with the previous ciphertext block before encryption, linking all blocks into a chain.

### PKCS#7 Padding

Pads plaintext so its length is an exact multiple of the block size (16 bytes):
- Append $N$ bytes each with value $N$, where $N = 16 - (\text{len} \bmod 16)$.
- If already aligned, append a full block of 16 × `0x10`.

**Example:** `"HELLO"` (5 bytes) → append 11 × `0x0B` → 16 bytes total.

### The Padding Oracle

A function that decrypts a ciphertext and returns only:
```
True   →  valid PKCS#7 padding
False  →  invalid padding
```

### Why It's Dangerous

From the CBC decryption equation:

$$P_i[j] = \text{AES\_DEC}(C_i)[j] \oplus C_{i-1}[j]$$

The attacker **controls** $C_{i-1}[j]$. By modifying it and querying the oracle, they can compute $\text{AES\_DEC}(C_i)[j]$ and recover $P_i[j]$ — one byte at a time — **without ever knowing the AES key.**

---

## 3. Task 2 — Attack Implementation

### Attack Algorithm (per block)

For each target block $C_i$, bytes are recovered **right-to-left** (byte 15 → 0):

1. Choose target padding value: $\text{pad} = 16 - j$ (for byte position $j$)
2. Fix already-recovered bytes at positions $k > j$: set $C'[k] = I[k] \oplus \text{pad}$
3. Brute-force $C'[j]$ through all 256 values (0–255)
4. When oracle returns `True`: $I[j] = C'[j] \oplus \text{pad}$
5. Compute plaintext: $P[j] = I[j] \oplus C_{i-1}[j]$

### Required Functions Implemented

| # | Function | Purpose |
|---|:---|:---|
| 1 | `pkcs7_pad()` | Applies PKCS#7 padding to plaintext |
| 2 | `pkcs7_unpad()` | Strips and validates PKCS#7 padding |
| 3 | `has_valid_padding()` | Checks padding validity without raising exceptions |
| 4 | `encrypt()` | AES-CBC encryption with random IV (key hidden) |
| 5 | `decrypt_raw()` | AES-CBC decryption returning raw bytes incl. padding |
| 6 | `decrypt()` | AES-CBC decryption with padding stripped |
| 7 | `padding_oracle()` | Returns True iff decrypted ciphertext has valid padding |
| 8 | `recover_intermediate_block()` | Recovers all 16 intermediate bytes for a block |
| 9 | `recover_block_plaintext()` | XORs intermediate bytes with prev block to get plaintext |
| 10 | `padding_oracle_attack()` | Orchestrates full multi-block attack and strips padding |

---

## 4. Task 3 — Attack Analysis

### Oracle Query Count

For a ciphertext with $N$ blocks:

| Metric | Formula | Example ($N=4$ blocks) |
|:---:|:---:|:---:|
| Worst-case  | $256 \times 16 \times N$ | 16,384 queries |
| Average     | $128 \times 16 \times N$ | 8,192 queries |
| Actual (measured) | depends on key/data | ~7,000–9,000 queries |

### Why Modifying $C_{i-1}$ Affects $P_i$

The decryption equation is:

$$P_i[j] = \underbrace{\text{AES\_DEC}(C_i)[j]}_{\text{fixed (attacker can't change }C_i)} \oplus \underbrace{C_{i-1}[j]}_{\text{attacker controls this}}$$

Since $\text{AES\_DEC}(C_i)$ is deterministic and $C_i$ is unchanged, flipping any bit in $C_{i-1}[j]$ causes a **predictable, deterministic XOR flip** in $P_i[j]$. This gives the attacker full control over the decrypted byte — which they exploit to force valid padding patterns.

---

## 5. Task 4 — Security Recommendations

| Priority | Fix | Notes |
|:---:|:---|:---|
| ⭐ 1 (Best) | **Authenticated Encryption (AES-GCM)** | Verifies auth tag before decryption — no padding ever checked |
| 2 | **Encrypt-then-MAC (HMAC-SHA256)** | MAC checked before decryption; use `hmac.compare_digest` |
| 3 | **Constant-time error responses** | All errors (bad MAC, bad padding) must look identical |
| 4 | **Constant-time padding validation** | Never branch on individual padding bytes |
| 5 | **TLS 1.3** | Removes CBC entirely; mandates AES-GCM / ChaCha20-Poly1305 |

---

## 6. Experimental Results (Group 10 Assignment Message)

**Message:** `CryptoLabX Group 10 Secret Message for Padding Oracle Lab!`  
**Ciphertext:** 64 bytes (4 blocks)

| Metric | Value |
|:---|:---:|
| Recovered Plaintext | ✅ Exact Match |
| Oracle Queries Used | ~7,000–8,500 |
| Worst-case Maximum | 16,384 |
| Efficiency Saving | ~48% fewer queries than worst-case |

---

## 7. Project Structure

```
attacks/padding_oracle_attack/
├── src/
│   ├── aes_cbc.py              # AES-CBC encrypt/decrypt + PKCS#7 helpers
│   ├── padding_oracle_attack.py # Core attack implementation
│   ├── main.py                 # Interactive CLI driver
│   └── __init__.py
├── testcases/
│   ├── messages.json           # Predefined test messages
│   └── test_padding_oracle.py  # Unit test suite (17 tests)
├── outputs/
│   └── results.txt             # Auto-saved attack results
├── reports/
├── screenshots/
└── README.md
```

---

## 8. Execution Instructions

### Run Automated Evaluation (Group 10 Dataset):
```powershell
python attacks/padding_oracle_attack/src/main.py --auto
```

### Run Interactive Menu:
```powershell
python attacks/padding_oracle_attack/src/main.py
```

Menu options:
- `[1]` Explain the Attack (Theory)
- `[2]` Run Attack on Group 10 Test Message
- `[3]` Run Attack on All Predefined Messages
- `[4]` Custom Plaintext Attack
- `[5]` Security Recommendations
- `[6]` Exit

### Run Unit Tests:
```powershell
python attacks/padding_oracle_attack/testcases/test_padding_oracle.py
```

---

## 9. Key Constraints Met

| Constraint | Status |
|:---|:---:|
| AES key NOT used or accessed during attack | ✅ Key lives only in `aes_cbc._KEY` (unexported) |
| No ready-made padding oracle attack library used | ✅ Implemented from scratch |
| Solution works for any ciphertext (not hardcoded) | ✅ Fully generic algorithm |
| PKCS#7 padding library used for enc/dec only | ✅ `pycryptodome` used only for AES primitive |

---

## 10. Dependencies

```
pycryptodome>=3.0
```

Install:
```powershell
pip install pycryptodome
```
