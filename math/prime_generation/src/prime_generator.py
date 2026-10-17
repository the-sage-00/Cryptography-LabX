"""
CryptoLabX - Cryptographic Prime Generator Module
Course: Cryptography Laboratory (22CPP307)
Group: 10

Generates cryptographically strong prime candidates of arbitrary bit lengths (default 512-bit)
using cryptographically secure random bitstreams, trial-division pre-filtering,
and Miller-Rabin primality testing.
"""

import secrets
import time
from typing import Dict, List, Tuple
try:
    from .miller_rabin import miller_rabin_test
except ImportError:
    from miller_rabin import miller_rabin_test


def get_small_primes(limit: int = 1000) -> List[int]:
    """
    Generate prime numbers up to a specified limit using the Sieve of Eratosthenes.
    Used for rapid pre-filtering of composite candidates before modular exponentiation.
    """
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for p in range(2, int(limit ** 0.5) + 1):
        if sieve[p]:
            for i in range(p * p, limit + 1, p):
                sieve[i] = False
    return [p for p in range(2, limit + 1) if sieve[p]]


SMALL_PRIMES = get_small_primes(1000)


def generate_candidate(bit_length: int = 512) -> int:
    """
    Generate a random odd integer candidate of EXACTLY the assigned bit length.

    Cryptographic Properties:
      1. Cryptographically secure random bitstream from OS entropy pool via `secrets.randbits`.
      2. Most Significant Bit (MSB, bit index bit_length - 1) is forced to 1.
         This strictly guarantees 2^(bit_length - 1) <= candidate < 2^(bit_length)
         and ensures candidate.bit_length() == bit_length.
      3. Least Significant Bit (LSB, bit index 0) is forced to 1.
         This guarantees the candidate is odd, eliminating all even composite numbers.

    Args:
        bit_length: Target bit length (default 512).

    Returns:
        Odd integer candidate of exact bit length.
    """
    if bit_length < 2:
        raise ValueError("Bit length must be at least 2")

    candidate = secrets.randbits(bit_length)
    candidate |= (1 << (bit_length - 1))  # Force MSB = 1 (exact bit length)
    candidate |= 1                        # Force LSB = 1 (odd integer)
    return candidate


def pre_filter_small_primes(candidate: int) -> bool:
    """
    Quick trial-division filter using precomputed primes up to 1000.

    Filters out approximately 85% of composite candidates in microseconds,
    avoiding expensive 512-bit modular exponentiations.

    Args:
        candidate: Large odd integer.

    Returns:
        False if candidate is divisible by any small prime (definitely composite),
        True if candidate passes and requires full Miller-Rabin evaluation.
    """
    for prime in SMALL_PRIMES:
        if candidate == prime:
            return True
        if candidate % prime == 0:
            return False
    return True


def generate_prime(
    bit_length: int = 512,
    rounds: int = 40,
    use_prefilter: bool = True
) -> Dict:
    """
    Generate a probable prime integer of exact bit length using Miller-Rabin testing.

    Algorithm:
      1. Sample random odd candidate with MSB=1 and LSB=1.
      2. Rapidly filter with small prime trial division.
      3. If passed, execute Miller-Rabin test across `rounds` independent bases.
      4. If failed, increment counter and repeat.
      5. Once found, verify exact bit length and record metrics.

    Args:
        bit_length: Assigned bit length (default 512).
        rounds: Number of Miller-Rabin rounds (default 40 for error <= 2^-80).
        use_prefilter: Enable trial division pre-filtering (default True).

    Returns:
        Dictionary containing all experimental metrics required for laboratory submission:
          - assigned_bit_length
          - actual_bit_length
          - generated_prime
          - prime_hex
          - candidates_tested
          - mr_rounds
          - execution_time_seconds
          - execution_time_ms
    """
    start_time = time.perf_counter()
    candidates_tested = 0

    while True:
        candidates_tested += 1
        candidate = generate_candidate(bit_length)

        # Pre-filter using small prime trial division
        if use_prefilter and not pre_filter_small_primes(candidate):
            continue

        # Full Miller-Rabin test across assigned rounds
        if miller_rabin_test(candidate, k=rounds):
            end_time = time.perf_counter()
            elapsed_sec = end_time - start_time
            actual_bits = candidate.bit_length()

            # Ensure strict assertion of assigned bit length
            assert actual_bits == bit_length, (
                f"Bit length mismatch: expected {bit_length}, got {actual_bits}"
            )

            return {
                "assigned_bit_length": bit_length,
                "actual_bit_length": actual_bits,
                "generated_prime": candidate,
                "prime_hex": hex(candidate),
                "candidates_tested": candidates_tested,
                "mr_rounds": rounds,
                "execution_time_seconds": elapsed_sec,
                "execution_time_ms": elapsed_sec * 1000.0,
            }
