"""
CryptoLabX - Miller-Rabin Primality Test Module
Course: Cryptography Laboratory (22CPP307)
Group: 10

Implements the Miller-Rabin probabilistic primality test, integer decomposition,
round verification, and cross-validation against independent cryptosystems.
"""

import secrets
from typing import Dict, List, Tuple


def decompose_n_minus_one(n: int) -> Tuple[int, int]:
    """
    Decompose n - 1 into 2^s * d, where d is odd and s >= 1.

    Args:
        n: An odd integer greater than 2.

    Returns:
        (s, d) such that n - 1 = (2 ** s) * d with d % 2 == 1.
    """
    if n <= 2 or n % 2 == 0:
        raise ValueError(f"Decomposition requires an odd integer > 2, got {n}")

    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2
    return s, d


def miller_rabin_single_base(n: int, a: int, s: int = None, d: int = None) -> bool:
    """
    Test candidate n with a single base 'a' under the Miller-Rabin algorithm.

    Conditions for n to be probable prime to base a:
      1. a^d = 1 (mod n), OR
      2. a^(d * 2^r) = -1 = n - 1 (mod n) for some 0 <= r < s.

    Args:
        n: Candidate odd integer.
        a: Base witness, 2 <= a <= n - 2.
        s: Power of 2 from decomposition (optional, computed if None).
        d: Odd component from decomposition (optional, computed if None).

    Returns:
        True if n passes Miller-Rabin for base a, False if composite.
    """
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    if s is None or d is None:
        s, d = decompose_n_minus_one(n)

    # Compute x = a^d mod n using fast binary modular exponentiation
    x = pow(a, d, n)

    if x == 1 or x == n - 1:
        return True

    # Repeatedly square x up to s - 1 times
    for _ in range(s - 1):
        x = pow(x, 2, n)
        if x == n - 1:
            return True
        if x == 1:
            # Non-trivial square root of 1 modulo n proves n is composite
            return False

    return False


def miller_rabin_test(n: int, k: int = 40) -> bool:
    """
    Execute k independent rounds of the Miller-Rabin primality test
    using cryptographically secure random bases.

    Error Probability:
      A composite number passes k rounds with probability <= 4^(-k).
      For k = 40, error probability <= 4^(-40) = 2^(-80) < 8.27 * 10^(-25).

    Args:
        n: The odd integer candidate to test.
        k: Number of independent test rounds (default 40).

    Returns:
        True if n is a probable prime, False if n is definitively composite.
    """
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    s, d = decompose_n_minus_one(n)

    for _ in range(k):
        # Choose a random base a in [2, n - 2]
        a = secrets.randbelow(n - 3) + 2
        if not miller_rabin_single_base(n, a, s, d):
            return False

    return True


def verify_with_specified_bases(n: int, bases: List[int]) -> List[Dict]:
    """
    Verify candidate n against a specific, deterministic list of bases
    and record step-by-step diagnostic information for laboratory demonstration.

    Args:
        n: Candidate odd integer.
        bases: List of integer bases (e.g., [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]).

    Returns:
        List of dicts containing base, initial x = a^d mod n, passed flag, and condition.
    """
    s, d = decompose_n_minus_one(n)
    records = []

    for base in bases:
        if base >= n:
            continue

        x = pow(base, d, n)
        passed = False
        condition = ""

        if x == 1:
            passed = True
            condition = "a^d = 1 (mod n)"
        elif x == n - 1:
            passed = True
            condition = "a^d = -1 (mod n)"
        else:
            cur_x = x
            for r in range(1, s):
                cur_x = pow(cur_x, 2, n)
                if cur_x == n - 1:
                    passed = True
                    condition = f"a^(d * 2^{r}) = -1 (mod n)"
                    break
                if cur_x == 1:
                    condition = f"Non-trivial root of 1 at round {r}"
                    break
            if not passed and not condition:
                condition = "No power yielded -1 (mod n)"

        records.append({
            "base": base,
            "passed": passed,
            "condition": condition,
            "initial_x_preview": hex(x)[:16] + "..."
        })

    return records


def verify_with_trusted_library(n: int) -> bool:
    """
    Verify candidate primality using an independent, trusted cryptographic library
    (PyCryptodome's isPrime method).

    Args:
        n: Integer candidate.

    Returns:
        True if library confirms primality, False otherwise.
    """
    try:
        from Crypto.Util.number import isPrime
        return bool(isPrime(n))
    except ImportError:
        # Fallback to internal high-round check if library not present
        return miller_rabin_test(n, k=64)
