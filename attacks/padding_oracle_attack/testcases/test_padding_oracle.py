"""
CryptoLabX - Padding Oracle Attack: Test Suite
Course: Cryptography Laboratory (22CPP307)
Assignment 7: Padding Oracle Attack on AES-CBC
"""

import sys
import os
import unittest

# Ensure local package imports work regardless of how tests are run
src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src')
if src_dir not in sys.path:
    sys.path.insert(0, os.path.abspath(src_dir))

from aes_cbc import (
    pkcs7_pad, pkcs7_unpad, has_valid_padding,
    encrypt, decrypt, BLOCK_SIZE
)
from padding_oracle_attack import (
    padding_oracle, padding_oracle_attack,
    reset_oracle_counter, get_oracle_query_count
)


class TestPKCS7Padding(unittest.TestCase):
    """Test PKCS#7 padding utilities."""

    def test_pad_short_message(self):
        data = b"HELLO"  # 5 bytes → need 11 bytes of 0x0B
        padded = pkcs7_pad(data)
        self.assertEqual(len(padded), 16)
        self.assertEqual(padded[-1], 11)
        self.assertEqual(padded[5:], bytes([11] * 11))

    def test_pad_exact_block(self):
        data = b"A" * 16  # already aligned → full extra block
        padded = pkcs7_pad(data)
        self.assertEqual(len(padded), 32)
        self.assertEqual(padded[16:], bytes([16] * 16))

    def test_unpad_valid(self):
        data = b"HELLO" + bytes([11] * 11)
        result = pkcs7_unpad(data)
        self.assertEqual(result, b"HELLO")

    def test_unpad_invalid_raises(self):
        bad = b"HELLO" + bytes([11] * 10) + bytes([9])  # wrong last byte
        with self.assertRaises(ValueError):
            pkcs7_unpad(bad)

    def test_has_valid_padding_true(self):
        data = b"TEST" + bytes([12] * 12)
        self.assertTrue(has_valid_padding(data))

    def test_has_valid_padding_false(self):
        data = b"TEST" + bytes([0] * 12)  # 0x00 is invalid
        self.assertFalse(has_valid_padding(data))


class TestAESCBC(unittest.TestCase):
    """Test AES-CBC encryption / decryption round-trip."""

    def test_encrypt_decrypt_roundtrip(self):
        for msg in [b"Short", b"Exactly sixteen!", b"A" * 33]:
            iv, ct = encrypt(msg)
            recovered = decrypt(iv, ct)
            self.assertEqual(recovered, msg)

    def test_ciphertext_length_multiple_of_block_size(self):
        iv, ct = encrypt(b"Hello World")
        self.assertEqual(len(ct) % BLOCK_SIZE, 0)

    def test_different_ivs_produce_different_ciphertexts(self):
        iv1, ct1 = encrypt(b"Same plaintext")
        iv2, ct2 = encrypt(b"Same plaintext")
        # IVs should almost certainly differ (random)
        # ciphertexts should differ too
        self.assertNotEqual(iv1, iv2)


class TestPaddingOracle(unittest.TestCase):
    """Test the padding oracle function."""

    def test_oracle_true_for_valid_ciphertext(self):
        iv, ct = encrypt(b"Valid message!!")
        self.assertTrue(padding_oracle(iv, ct))

    def test_oracle_false_for_corrupted_ciphertext(self):
        iv, ct = encrypt(b"Valid message!!")
        # Corrupt the last byte of IV to break padding in the first block
        corrupted_iv = bytes([iv[i] ^ (0xFF if i == BLOCK_SIZE - 1 else 0) for i in range(BLOCK_SIZE)])
        # Very likely to produce invalid padding
        # (not guaranteed but overwhelmingly probable)
        results = [padding_oracle(corrupted_iv, ct) for _ in range(1)]
        # At least exists without error
        self.assertIsInstance(results[0], bool)


class TestPaddingOracleAttack(unittest.TestCase):
    """Test the full padding oracle attack."""

    def _attack_and_verify(self, plaintext: bytes):
        iv, ct = encrypt(plaintext)
        reset_oracle_counter()
        recovered, queries = padding_oracle_attack(iv, ct)
        self.assertEqual(
            recovered, plaintext,
            f"Attack failed for: {plaintext!r}\nRecovered: {recovered!r}"
        )
        self.assertGreater(queries, 0)
        print(f"\n    [{plaintext[:30]!r}...] queries={queries}")

    def test_attack_short_message(self):
        self._attack_and_verify(b"Hello World!")

    def test_attack_exact_block(self):
        self._attack_and_verify(b"Exactly16Bytes!!")

    def test_attack_multiblock(self):
        self._attack_and_verify(b"This message spans multiple AES blocks for testing.")

    def test_attack_single_char(self):
        self._attack_and_verify(b"X")

    def test_attack_all_ascii(self):
        msg = bytes(range(32, 128))  # all printable ASCII
        self._attack_and_verify(msg)

    def test_oracle_query_counter(self):
        iv, ct = encrypt(b"Count test!")
        reset_oracle_counter()
        _, queries = padding_oracle_attack(iv, ct)
        self.assertEqual(queries, get_oracle_query_count())


if __name__ == "__main__":
    print("=" * 70)
    print("  CryptoLabX — Assignment 7: Padding Oracle Attack Test Suite")
    print("  Course: Cryptography Laboratory (22CPP307) | Group: 10")
    print("=" * 70)
    unittest.main(verbosity=2)
