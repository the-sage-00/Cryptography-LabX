"""
CryptoLabX - Padding Oracle Attack Main Driver
Course: Cryptography Laboratory (22CPP307)
Assignment 7: Padding Oracle Attack on AES-CBC
Group: 10 (Even Group Number)

Interactive CLI driver that:
1. Encrypts predefined test messages using AES-CBC (key hidden).
2. Runs the Padding Oracle Attack to recover plaintext.
3. Reports oracle query counts and analysis.
4. Provides an interactive menu for custom inputs.
"""

import os
import sys
import json

# Fix Windows terminal encoding
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Ensure local package imports work regardless of current working directory
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from aes_cbc import encrypt, decrypt, BLOCK_SIZE
from padding_oracle_attack import padding_oracle_attack, padding_oracle

# ── Paths ─────────────────────────────────────────────────────────────────────
DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "testcases", "messages.json"
)
OUTPUT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "outputs", "results.txt"
)


# ─────────────────────────────────────────────────────────────────────────────
# Banner
# ─────────────────────────────────────────────────────────────────────────────

def print_banner() -> None:
    print("=" * 78)
    print("             PADDING ORACLE ATTACK ON AES-CBC")
    print("         Course: Cryptography Laboratory (22CPP307) | Group: 10")
    print("=" * 78)


# ─────────────────────────────────────────────────────────────────────────────
# Theory Section (Task 1)
# ─────────────────────────────────────────────────────────────────────────────

def print_theory() -> None:
    print("""
┌─────────────────────────────────────────────────────────────────────────────┐
│  TASK 1 — UNDERSTANDING THE ATTACK                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  AES-CBC (Cipher Block Chaining)                                            │
│  ─────────────────────────────────                                          │
│  Encryption:   C_i = AES_ENC(P_i XOR C_{i-1}),   C_0 = IV                 │
│  Decryption:   P_i = AES_DEC(C_i) XOR C_{i-1},   C_0 = IV                 │
│                                                                             │
│  Each plaintext block is XOR-ed with the previous ciphertext block (or IV) │
│  before encryption, chaining blocks together.                               │
│                                                                             │
│  PKCS#7 Padding                                                             │
│  ──────────────                                                             │
│  Pads plaintext so its length is a multiple of the block size (16 bytes).  │
│  N bytes of value N are appended:                                           │
│    "HELLO" (5 bytes) → appends 11 × 0x0B → 16 bytes total.                 │
│  If already aligned, a full block of 16 × 0x10 is added.                   │
│                                                                             │
│  The Padding Oracle                                                         │
│  ──────────────────                                                         │
│  A service that decrypts a ciphertext and answers ONE question:             │
│      "Is the padding of the decrypted message valid?"  (True / False)       │
│                                                                             │
│  Why It's Dangerous                                                         │
│  ──────────────────                                                         │
│  AES-CBC decryption of block i:                                             │
│      P_i[j] = AES_DEC(C_i)[j]  XOR  C_{i-1}[j]                            │
│  The attacker controls C_{i-1}[j].  By systematically modifying it and     │
│  querying the oracle, they can recover AES_DEC(C_i)[j] — and hence P_i[j] │
│  — one byte at a time, without ever knowing the AES key.                   │
│                                                                             │
│  Worst-case oracle queries: 256 × (BLOCK_SIZE) × (num_blocks)              │
│  = 256 × 16 × N ≈ 4096 × N queries for N ciphertext blocks.                │
└─────────────────────────────────────────────────────────────────────────────┘
""")


# ─────────────────────────────────────────────────────────────────────────────
# Analysis Section (Task 3)
# ─────────────────────────────────────────────────────────────────────────────

def print_analysis(queries: int, num_blocks: int, plaintext_len: int) -> None:
    print("\n" + "─" * 78)
    print("TASK 3 — ATTACK ANALYSIS")
    print("─" * 78)
    max_possible  = 256 * BLOCK_SIZE * num_blocks
    theoretical   = 128 * BLOCK_SIZE * num_blocks   # average (128 per byte)
    efficiency_pct = (1 - queries / max_possible) * 100 if max_possible else 0

    print(f"""
  Recovered Plaintext Length : {plaintext_len} bytes
  Ciphertext Blocks Attacked : {num_blocks}
  Oracle Queries Used        : {queries:,}
  Theoretical Maximum        : {max_possible:,}  (256 × 16 × {num_blocks})
  Statistical Average        : {theoretical:,}  (128 × 16 × {num_blocks})
  Efficiency Savings         : {efficiency_pct:.1f}% fewer queries than worst-case

  Why Modifying C_{{i-1}} Affects P_i
  ─────────────────────────────────
  From the CBC decryption equation:
      P_i[j] = AES_DEC(C_i)[j]  XOR  C_{{i-1}}[j]

  AES_DEC(C_i) is a fixed value (since C_i is unchanged).
  Therefore flipping any bit in C_{{i-1}} causes a predictable, deterministic
  change in the corresponding byte of P_i.  The attacker exploits this to
  force P_i to produce any desired padding pattern.

  Oracle Query Budget per Byte
  ─────────────────────────────
  Each plaintext byte requires at most 256 oracle queries (brute force 0-255).
  On average ~128 queries are needed (uniform distribution).
  Total bytes recovered: {num_blocks * BLOCK_SIZE}
""")


# ─────────────────────────────────────────────────────────────────────────────
# Security Recommendations (Task 4)
# ─────────────────────────────────────────────────────────────────────────────

def print_security_recommendations() -> None:
    print("─" * 78)
    print("TASK 4 — SECURITY RECOMMENDATIONS")
    print("─" * 78)
    print("""
  The padding oracle vulnerability arises when a system leaks whether
  decryption produced valid padding.  Prevention strategies:

  1. Authenticated Encryption (AE) — RECOMMENDED
     ─────────────────────────────────────────────
     Use AES-GCM, AES-CCM, or ChaCha20-Poly1305.  The authentication tag
     is verified BEFORE decryption.  Invalid ciphertexts are rejected
     immediately — no padding check is ever reached.
     ► Standard libraries (Python's `cryptography`, OpenSSL, libsodium)
       provide AE modes by default.

  2. Encrypt-then-MAC
     ─────────────────
     Apply HMAC-SHA256 to the ciphertext AFTER encryption.  Verify the MAC
     before attempting decryption.  A forged/modified ciphertext fails the
     MAC check before any decryption occurs.
     ► Constant-time MAC comparison (hmac.compare_digest) prevents
       timing-side-channel leaks.

  3. Constant-Time Error Responses
     ─────────────────────────────
     If CBC-with-padding must be used, ensure ALL error paths (padding error,
     MAC error, decryption error) return the SAME error code after the SAME
     time delay.  Never expose a distinct "bad padding" error.

  4. Eliminate PKCS#7 Padding Side-Channels
     ────────────────────────────────────────
     Validate padding in constant time:
         def constant_time_padding_check(data):
             pad = data[-1]
             mask = 0
             for b in data[-pad:]:
                 mask |= b ^ pad
             return mask == 0

  5. Adopt TLS 1.3 / Modern Protocols
     ───────────────────────────────────
     TLS 1.3 mandates AES-GCM or ChaCha20-Poly1305 — CBC mode is removed
     entirely, eliminating the attack surface.

  Summary
  ───────
  The safest fix is authenticated encryption (AES-GCM).  It is faster,
  simpler, and immune to padding oracle, bit-flipping, and replay attacks.
""")


# ─────────────────────────────────────────────────────────────────────────────
# Run a Single Attack Scenario
# ─────────────────────────────────────────────────────────────────────────────

def run_attack_scenario(label: str, plaintext_bytes: bytes) -> dict:
    """Encrypt a message, run the attack, and report results."""
    print("\n" + "═" * 78)
    print(f"  SCENARIO: {label}")
    print("═" * 78)

    print(f"\n  Original Plaintext   : {plaintext_bytes.decode('utf-8', errors='replace')}")
    print(f"  Plaintext Length     : {len(plaintext_bytes)} bytes")

    # Encrypt (key hidden inside aes_cbc module)
    iv, ciphertext = encrypt(plaintext_bytes)
    num_blocks = len(ciphertext) // BLOCK_SIZE

    print(f"\n  IV (hex)             : {iv.hex()}")
    print(f"  Ciphertext (hex)     : {ciphertext.hex()}")
    print(f"  Ciphertext Length    : {len(ciphertext)} bytes ({num_blocks} blocks)")
    print(f"\n  ⚠  The AES key is NOT used or printed anywhere below.")
    print(f"     Only the padding oracle's True/False response is used.\n")

    # Run Padding Oracle Attack
    print("─" * 78)
    print("  TASK 2 — RUNNING THE PADDING ORACLE ATTACK")
    print("─" * 78)

    recovered_pt, queries = padding_oracle_attack(iv, ciphertext)

    print(f"\n  [✓] Recovered Plaintext : {recovered_pt.decode('utf-8', errors='replace')}")
    print(f"  [✓] Oracle Queries Used : {queries:,}")

    # Verify correctness
    match = (recovered_pt == plaintext_bytes)
    print(f"  [✓] Match with Original : {'YES — 100% EXACT MATCH' if match else 'NO — MISMATCH'}")

    # Analysis
    print_analysis(queries, num_blocks, len(recovered_pt))

    return {
        "label"       : label,
        "plaintext"   : plaintext_bytes.decode('utf-8', errors='replace'),
        "iv_hex"      : iv.hex(),
        "ct_hex"      : ciphertext.hex(),
        "ct_len"      : len(ciphertext),
        "num_blocks"  : num_blocks,
        "recovered_pt": recovered_pt.decode('utf-8', errors='replace'),
        "queries"     : queries,
        "match"       : match,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Save Results
# ─────────────────────────────────────────────────────────────────────────────

def save_results(results: list[dict]) -> None:
    """Save all scenario results to outputs/results.txt."""
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    lines = [
        "=" * 80,
        "      PADDING ORACLE ATTACK ON AES-CBC — EXPERIMENTAL RESULTS",
        "         Course: Cryptography Laboratory (22CPP307) | Group: 10",
        "=" * 80,
        "",
    ]

    for r in results:
        lines += [
            f"Scenario       : {r['label']}",
            f"Plaintext      : {r['plaintext']}",
            f"IV (hex)       : {r['iv_hex']}",
            f"Ciphertext     : {r['ct_hex']}",
            f"CT Length      : {r['ct_len']} bytes ({r['num_blocks']} blocks)",
            f"Recovered PT   : {r['recovered_pt']}",
            f"Oracle Queries : {r['queries']:,}",
            f"Exact Match    : {'YES' if r['match'] else 'NO'}",
            "",
            "-" * 80,
            "",
        ]

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"\n[+] Full results saved to:\n    {OUTPUT_PATH}")


# ─────────────────────────────────────────────────────────────────────────────
# Interactive Menu
# ─────────────────────────────────────────────────────────────────────────────

def run_assignment() -> None:
    """Main interactive driver."""
    print_banner()

    # Load predefined messages
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {"messages": []}

    while True:
        print("\n" + "=" * 60)
        print("  ASSIGNMENT 7 INTERACTIVE MENU:")
        print("=" * 60)
        print("  [1] Explain the Attack (Theory)")
        print("  [2] Run Attack on Group 10 Test Message")
        print("  [3] Run Attack on All Predefined Messages")
        print("  [4] Custom Plaintext Attack")
        print("  [5] Security Recommendations")
        print("  [6] Exit")
        print("=" * 60)

        choice = input("  Select an option (1-6): ").strip()

        if choice == "1":
            print_theory()

        elif choice == "2":
            # Group 10 assigned message
            msg = data.get("messages", [{}])[0].get(
                "plaintext",
                "CryptoLabX Group 10 Secret Message for Padding Oracle Lab!"
            )
            result = run_attack_scenario("Group 10 Assigned Message", msg.encode('utf-8'))
            save_results([result])

        elif choice == "3":
            messages = data.get("messages", [])
            if not messages:
                print("  [!] No messages found in testcases/messages.json")
                continue
            results = []
            for entry in messages:
                r = run_attack_scenario(entry["label"], entry["plaintext"].encode('utf-8'))
                results.append(r)
            save_results(results)
            print_security_recommendations()

        elif choice == "4":
            custom_pt = input("\n  Enter plaintext to encrypt and attack: ").strip()
            if not custom_pt:
                print("  [!] Plaintext cannot be empty.")
                continue
            result = run_attack_scenario("Custom User Plaintext", custom_pt.encode('utf-8'))
            save_results([result])

        elif choice == "5":
            print_security_recommendations()

        elif choice == "6":
            print("\n  Exiting Padding Oracle Attack Toolkit. Goodbye!\n")
            break

        else:
            print("  [!] Invalid choice. Please choose 1 to 6.")


# ─────────────────────────────────────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        print_banner()
        print_theory()

        if os.path.exists(DATA_PATH):
            with open(DATA_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {"messages": []}

        messages = data.get("messages", [])
        results = []
        for entry in messages:
            r = run_attack_scenario(entry["label"], entry["plaintext"].encode('utf-8'))
            results.append(r)

        save_results(results)
        print_security_recommendations()
    else:
        run_assignment()
