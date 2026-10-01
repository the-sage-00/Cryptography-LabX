"""
CryptoLabX - AES-CBC Encryption / Decryption Helper
Course: Cryptography Laboratory (22CPP307)
Assignment 7: Padding Oracle Attack on AES-CBC

Provides AES-CBC encrypt / decrypt utilities using PKCS#7 padding.
The AES key is ONLY used inside this module — the attack code must
never import or access `KEY` directly.
"""

import os
from Crypto.Cipher import AES

# ── Block size constant ───────────────────────────────────────────────────────
BLOCK_SIZE = 16   # AES block size in bytes (128-bit)

# ── Secret key (hidden from the attacker — NOT exported) ─────────────────────
_KEY: bytes = os.urandom(BLOCK_SIZE)   # Randomly generated at runtime


# ─────────────────────────────────────────────────────────────────────────────
# PKCS#7 Padding helpers
# ─────────────────────────────────────────────────────────────────────────────

def pkcs7_pad(data: bytes, block_size: int = BLOCK_SIZE) -> bytes:
    """
    Apply PKCS#7 padding to *data* so its length is a multiple of *block_size*.

    PKCS#7 rule: append N bytes each with value N, where
        N = block_size - (len(data) % block_size).
    If the data is already a multiple of block_size, a full block of padding
    (all bytes = block_size) is appended.

    Example (block_size=16):
        "HELLO" (5 bytes) → appends 11 bytes of 0x0b → total 16 bytes.
    """
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len] * pad_len)


def pkcs7_unpad(data: bytes, block_size: int = BLOCK_SIZE) -> bytes:
    """
    Remove PKCS#7 padding from *data*.

    Raises ValueError if the padding is invalid.
    """
    if not data:
        raise ValueError("Empty data — cannot unpad.")
    pad_len = data[-1]
    if pad_len == 0 or pad_len > block_size:
        raise ValueError(f"Invalid PKCS#7 padding byte: {pad_len}")
    if data[-pad_len:] != bytes([pad_len] * pad_len):
        raise ValueError("Corrupt PKCS#7 padding — bytes do not match.")
    return data[:-pad_len]


def has_valid_padding(data: bytes, block_size: int = BLOCK_SIZE) -> bool:
    """
    Return True if *data* has valid PKCS#7 padding, False otherwise.
    Does NOT raise exceptions — intended for use as an oracle signal.
    """
    try:
        pkcs7_unpad(data, block_size)
        return True
    except ValueError:
        return False


# ─────────────────────────────────────────────────────────────────────────────
# AES-CBC Encryption / Decryption  (key is hidden inside this module)
# ─────────────────────────────────────────────────────────────────────────────

def encrypt(plaintext: bytes) -> tuple[bytes, bytes]:
    """
    Encrypt *plaintext* with AES-CBC using a random IV and the hidden key.

    Returns
    -------
    iv : bytes
        The randomly generated 16-byte IV.
    ciphertext : bytes
        The AES-CBC encrypted ciphertext (padded to a multiple of 16 bytes).
    """
    padded = pkcs7_pad(plaintext)
    iv = os.urandom(BLOCK_SIZE)
    cipher = AES.new(_KEY, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(padded)
    return iv, ciphertext


def decrypt_raw(iv: bytes, ciphertext: bytes) -> bytes:
    """
    Decrypt *ciphertext* with AES-CBC (hidden key, given IV).

    Returns the raw decrypted bytes INCLUDING the PKCS#7 padding.
    The caller is responsible for validation / removal of padding.
    """
    cipher = AES.new(_KEY, AES.MODE_CBC, iv)
    return cipher.decrypt(ciphertext)


def decrypt(iv: bytes, ciphertext: bytes) -> bytes:
    """
    Decrypt *ciphertext* with AES-CBC and strip valid PKCS#7 padding.

    Raises ValueError if the padding is invalid.
    """
    raw = decrypt_raw(iv, ciphertext)
    return pkcs7_unpad(raw)
