"""
CryptoLabX - Padding Oracle Attack Implementation
Course: Cryptography Laboratory (22CPP307)
Assignment 7: Padding Oracle Attack on AES-CBC
Group: 10 (Even Group Number)

Implements the complete Padding Oracle Attack to recover AES-CBC plaintext
without access to the encryption key.

Theory
------
AES-CBC Decryption of block B_i:
    P_i  = AES_DEC(B_i)  XOR  B_{i-1}      (B_0 = IV)

PKCS#7 Padding Oracle:
    The oracle returns True iff the decrypted ciphertext ends with valid
    PKCS#7 padding.  This single bit of information is sufficient to recover
    every plaintext byte.

Attack intuition (byte-by-byte, right to left inside each block):
    Suppose we target byte at position j (0-indexed from the left of a block).
    We craft a fake "previous block" C' such that:
        AES_DEC(B_i)[j] XOR C'[j] == desired_padding_value
    When the oracle returns True we know AES_DEC(B_i)[j] and can compute P[j].
"""

from __future__ import annotations
import sys
import os

# Ensure local package imports work regardless of current working directory
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from aes_cbc import decrypt_raw, has_valid_padding, BLOCK_SIZE
from typing import List, Tuple


# ─────────────────────────────────────────────────────────────────────────────
# Padding Oracle
# ─────────────────────────────────────────────────────────────────────────────

_oracle_query_count: int = 0   # Module-level counter


def padding_oracle(iv: bytes, ciphertext: bytes) -> bool:
    """
    The Padding Oracle.

    Decrypts *ciphertext* with the given *iv* and returns True iff the result
    has valid PKCS#7 padding.

    Constraints
    -----------
    * The AES key is NEVER exposed — it lives inside aes_cbc._KEY only.
    * This function does NOT return any plaintext — only a single boolean.
    * Every call to this function is counted for analysis purposes.
    """
    global _oracle_query_count
    _oracle_query_count += 1
    raw = decrypt_raw(iv, ciphertext)
    return has_valid_padding(raw)


def reset_oracle_counter() -> None:
    """Reset the global oracle query counter to zero."""
    global _oracle_query_count
    _oracle_query_count = 0


def get_oracle_query_count() -> int:
    """Return the current oracle query count."""
    return _oracle_query_count


# ─────────────────────────────────────────────────────────────────────────────
# Core Attack: Single Block Recovery
# ─────────────────────────────────────────────────────────────────────────────

def recover_intermediate_block(target_block: bytes, prev_block: bytes) -> List[int]:
    """
    Recover the AES intermediate bytes I for *target_block*.

    AES-CBC intermediate bytes:
        I[j] = AES_DEC(target_block)[j]

    Once we know I[j] we compute the plaintext byte:
        P[j] = I[j] XOR prev_block[j]

    Strategy (right-to-left byte recovery per PKCS#7):
        To recover byte at position j (0-indexed from left, so position
        BLOCK_SIZE-1 is the rightmost / last byte):
          1.  Fix already-recovered bytes i > j so the oracle sees valid
              padding for pad_value = BLOCK_SIZE - j.
          2.  Brute-force the 256 candidates for C'[j].
          3.  When the oracle returns True:
                  I[j] = C'[j] XOR pad_value
          4.  Compute P[j] = I[j] XOR prev_block[j].

    Returns
    -------
    intermediate : List[int]
        The 16 intermediate bytes I[0..15] for *target_block*.
    """
    # Work with mutable list; start with a copy of the real prev_block
    # (the crafted block C' that we will modify)
    crafted = bytearray(prev_block)
    intermediate = [0] * BLOCK_SIZE

    # Recover bytes from the LAST position to the FIRST (right → left)
    for byte_pos in range(BLOCK_SIZE - 1, -1, -1):
        pad_value = BLOCK_SIZE - byte_pos   # e.g. pos 15 → pad=1, pos 14 → pad=2 …

        # Fix already-recovered positions (those to the right of byte_pos)
        # so the oracle sees the correct trailing padding bytes.
        for k in range(byte_pos + 1, BLOCK_SIZE):
            crafted[k] = intermediate[k] ^ pad_value

        # Brute-force all 256 candidates for crafted[byte_pos]
        found = False
        for candidate in range(256):
            crafted[byte_pos] = candidate

            # Query the oracle: treat `crafted` as the "IV/previous block"
            # for `target_block`.
            if padding_oracle(bytes(crafted), target_block):
                # ── Disambiguation: Make sure we actually have pad_value=1
                #    and not an accidental longer valid padding.
                #    For pad_value=1 (last byte) only: flip the byte immediately
                #    before byte_pos and re-query.  If the oracle changes to
                #    False, this was a false positive; keep searching.
                if pad_value == 1 and byte_pos > 0:
                    crafted[byte_pos - 1] ^= 0xFF   # flip an earlier byte
                    still_valid = padding_oracle(bytes(crafted), target_block)
                    crafted[byte_pos - 1] ^= 0xFF   # restore
                    if not still_valid:
                        continue   # false positive — try next candidate

                # Compute intermediate byte:  I[j] = candidate XOR pad_value
                intermediate[byte_pos] = candidate ^ pad_value
                found = True
                break

        if not found:
            # Should not happen with a correct oracle; handle gracefully
            raise RuntimeError(
                f"Padding oracle attack failed at block byte position {byte_pos}. "
                "No valid candidate found — check oracle implementation."
            )

    return intermediate


def recover_block_plaintext(target_block: bytes, prev_block: bytes) -> bytes:
    """
    Recover the plaintext for *target_block* given its preceding block.

    P[j] = I[j] XOR prev_block[j]

    Parameters
    ----------
    target_block : bytes
        The 16-byte AES-CBC ciphertext block to decrypt.
    prev_block : bytes
        The 16-byte block immediately before *target_block* (or the IV for
        the first ciphertext block).

    Returns
    -------
    plaintext_block : bytes
        The 16 recovered plaintext bytes for *target_block*.
    """
    intermediate = recover_intermediate_block(target_block, prev_block)
    plaintext_block = bytes(
        intermediate[j] ^ prev_block[j] for j in range(BLOCK_SIZE)
    )
    return plaintext_block


# ─────────────────────────────────────────────────────────────────────────────
# Full Ciphertext Recovery
# ─────────────────────────────────────────────────────────────────────────────

def padding_oracle_attack(iv: bytes, ciphertext: bytes) -> Tuple[bytes, int]:
    """
    Recover the complete plaintext from an AES-CBC *ciphertext* using only
    the padding oracle — no key access.

    Algorithm
    ---------
    Split ciphertext into N blocks of BLOCK_SIZE bytes.
    For block i (1-indexed):
        prev_block = ciphertext[i-1]  (or IV for i=1)
        plaintext[i] = recover_block_plaintext(block[i], prev_block)
    Concatenate all plaintext blocks and strip PKCS#7 padding.

    Parameters
    ----------
    iv : bytes
        The 16-byte Initialization Vector used during encryption.
    ciphertext : bytes
        The full AES-CBC ciphertext (must be a multiple of BLOCK_SIZE).

    Returns
    -------
    plaintext : bytes
        The fully recovered plaintext with padding stripped.
    queries_used : int
        Total oracle queries consumed by this attack.
    """
    if len(ciphertext) % BLOCK_SIZE != 0:
        raise ValueError(
            f"Ciphertext length ({len(ciphertext)}) is not a multiple of "
            f"BLOCK_SIZE ({BLOCK_SIZE})."
        )

    reset_oracle_counter()

    num_blocks = len(ciphertext) // BLOCK_SIZE
    blocks = [ciphertext[i * BLOCK_SIZE:(i + 1) * BLOCK_SIZE]
              for i in range(num_blocks)]

    recovered_blocks: List[bytes] = []

    print(f"\n[+] Starting Padding Oracle Attack")
    print(f"    Ciphertext blocks : {num_blocks}")
    print(f"    Block size        : {BLOCK_SIZE} bytes")
    print(f"    Total bytes       : {len(ciphertext)}")

    for block_index in range(num_blocks):
        prev_block = iv if block_index == 0 else blocks[block_index - 1]
        target_block = blocks[block_index]

        print(f"\n    [*] Recovering Block {block_index + 1}/{num_blocks} ...", end="", flush=True)
        pt_block = recover_block_plaintext(target_block, prev_block)
        recovered_blocks.append(pt_block)

        # Show bytes recovered so far (printable chars only for display)
        display = ''.join(chr(b) if 32 <= b < 127 else '?' for b in pt_block)
        print(f" DONE  -> \"{display}\"")

    queries_used = get_oracle_query_count()

    # Concatenate all recovered plaintext blocks
    recovered_padded = b"".join(recovered_blocks)

    # Strip PKCS#7 padding
    try:
        from aes_cbc import pkcs7_unpad
        plaintext = pkcs7_unpad(recovered_padded)
    except ValueError:
        # Padding strip failed — return raw (should not happen normally)
        plaintext = recovered_padded

    return plaintext, queries_used
