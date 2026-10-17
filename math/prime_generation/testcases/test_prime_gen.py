"""
CryptoLabX - Unit Test Suite for Miller-Rabin Prime Generation
Course: Cryptography Laboratory (22CPP307)
Group: 10

Comprehensive test suite verifying integer decomposition, small prime accuracy,
Carmichael number detection, exact 512-bit bounds, and independent library verification.
"""

import os
import sys
import unittest

# Ensure local imports
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PRIME_GEN_DIR = os.path.dirname(TEST_DIR)
SRC_DIR = os.path.join(PRIME_GEN_DIR, "src")
MATH_DIR = os.path.dirname(PRIME_GEN_DIR)
REPO_ROOT = os.path.dirname(MATH_DIR)

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from miller_rabin import (
    decompose_n_minus_one,
    miller_rabin_single_base,
    miller_rabin_test,
    verify_with_specified_bases,
    verify_with_trusted_library,
)
from prime_generator import (
    generate_candidate,
    generate_prime,
    pre_filter_small_primes,
)


class TestMillerRabin(unittest.TestCase):
    """Test suite for Miller-Rabin primality testing algorithm."""

    def test_decompose_odd_integer(self):
        # 13 - 1 = 12 = 2^2 * 3 -> s=2, d=3
        s, d = decompose_n_minus_one(13)
        self.assertEqual(s, 2)
        self.assertEqual(d, 3)
        self.assertEqual((2 ** s) * d, 12)

        # 41 - 1 = 40 = 2^3 * 5 -> s=3, d=5
        s, d = decompose_n_minus_one(41)
        self.assertEqual(s, 3)
        self.assertEqual(d, 5)

    def test_decompose_raises_for_even(self):
        with self.assertRaises(ValueError):
            decompose_n_minus_one(10)
        with self.assertRaises(ValueError):
            decompose_n_minus_one(2)

    def test_known_small_primes(self):
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 97, 101, 1009]
        for p in primes:
            self.assertTrue(miller_rabin_test(p, k=10), f"Failed for known prime {p}")

    def test_known_composites(self):
        composites = [4, 6, 8, 9, 12, 15, 21, 25, 27, 33, 35, 49, 77, 91, 100, 1000]
        for c in composites:
            self.assertFalse(miller_rabin_test(c, k=10), f"Failed for known composite {c}")

    def test_carmichael_numbers_detected_as_composite(self):
        """
        Carmichael numbers pass Fermat's Little Theorem for all coprime bases,
        but MUST be detected as composite by Miller-Rabin.
        """
        carmichaels = [561, 1105, 1729, 2465, 2821, 6601]
        for cn in carmichaels:
            self.assertFalse(
                miller_rabin_test(cn, k=20),
                f"Miller-Rabin failed to detect Carmichael number {cn} as composite"
            )

    def test_specified_bases_evaluation(self):
        # Test 101 (prime) against bases [2, 3, 5, 7]
        results = verify_with_specified_bases(101, [2, 3, 5, 7])
        self.assertEqual(len(results), 4)
        for r in results:
            self.assertTrue(r["passed"], f"Base {r['base']} failed for prime 101")

        # Test 91 = 7 * 13 (composite)
        results = verify_with_specified_bases(91, [2, 3, 5])
        passed_any = any(r["passed"] for r in results)
        # 91 is a pseudoprime to base 9, but fails base 2 and 3
        results_b2 = [r for r in results if r["base"] == 2][0]
        self.assertFalse(results_b2["passed"])

    def test_trusted_library_verification(self):
        # 2^127 - 1 (12th Mersenne prime)
        mersenne_127 = (1 << 127) - 1
        self.assertTrue(miller_rabin_test(mersenne_127, k=20))
        self.assertTrue(verify_with_trusted_library(mersenne_127))


class TestPrimeGenerator(unittest.TestCase):
    """Test suite for candidate and 512-bit prime generation."""

    def test_candidate_exact_bit_length(self):
        for _ in range(50):
            c = generate_candidate(512)
            self.assertEqual(c.bit_length(), 512)

    def test_candidate_is_odd(self):
        for _ in range(50):
            c = generate_candidate(512)
            self.assertEqual(c % 2, 1)

    def test_candidate_mathematical_bounds(self):
        for _ in range(50):
            c = generate_candidate(512)
            self.assertGreaterEqual(c, 1 << 511)
            self.assertLess(c, 1 << 512)

    def test_prefilter_small_primes(self):
        self.assertFalse(pre_filter_small_primes(15))
        self.assertFalse(pre_filter_small_primes(77))
        self.assertTrue(pre_filter_small_primes(97))

    def test_generate_prime_512_full_pipeline(self):
        result = generate_prime(bit_length=512, rounds=40)
        p = result["generated_prime"]

        self.assertEqual(result["assigned_bit_length"], 512)
        self.assertEqual(result["actual_bit_length"], 512)
        self.assertEqual(p.bit_length(), 512)
        self.assertEqual(p % 2, 1)
        self.assertGreaterEqual(result["candidates_tested"], 1)
        self.assertGreater(result["execution_time_seconds"], 0.0)

        # Cross-verify with trusted library
        self.assertTrue(verify_with_trusted_library(p))

    def test_generate_prime_custom_bit_length(self):
        result = generate_prime(bit_length=256, rounds=30)
        p = result["generated_prime"]
        self.assertEqual(p.bit_length(), 256)
        self.assertTrue(verify_with_trusted_library(p))


if __name__ == "__main__":
    unittest.main(verbosity=2)
