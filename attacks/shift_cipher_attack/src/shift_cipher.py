"""
CryptoLabX - Shift Cipher Module
Course: Cryptography Laboratory (22CPP307)
Assignment 4: Cryptanalysis of Shift Cipher

This module implements Shift Cipher (Caesar Cipher) encryption and decryption.
Formula:
  Encryption : C = (P + k) mod 26
  Decryption : P = (C - k) mod 26
"""


def encrypt(plaintext: str, key: int) -> str:
    """
    Encrypt plaintext using Shift Cipher with key k.

    Args:
        plaintext: The input text to encrypt.
        key: Shift key (0-25).

    Returns:
        Ciphertext string.
    """
    key = key % 26
    ciphertext = []

    for char in plaintext:
        if char.isupper():
            shifted = chr((ord(char) - ord('A') + key) % 26 + ord('A'))
            ciphertext.append(shifted)
        elif char.islower():
            shifted = chr((ord(char) - ord('a') + key) % 26 + ord('a'))
            ciphertext.append(shifted)
        else:
            ciphertext.append(char)

    return "".join(ciphertext)


def decrypt(ciphertext: str, key: int) -> str:
    """
    Decrypt ciphertext using Shift Cipher with key k.

    Args:
        ciphertext: The encrypted text to decrypt.
        key: Shift key (0-25).

    Returns:
        Plaintext string.
    """
    return encrypt(ciphertext, -key)


if __name__ == "__main__":
    test_text = "Hello, World! CryptoLabX Assignment 4."
    test_key = 7
    encrypted = encrypt(test_text, test_key)
    decrypted = decrypt(encrypted, test_key)

    print(f"Original  : {test_text}")
    print(f"Key       : {test_key}")
    print(f"Encrypted : {encrypted}")
    print(f"Decrypted : {decrypted}")
    assert test_text == decrypted, "Decryption check failed!"
    print("Shift Cipher module test passed!")
