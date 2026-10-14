
# Padding Oracle Attack: Query Count Analysis

## Aim

To study how plaintext length affects the number of oracle queries required by the AES-CBC Padding Oracle Attack.

## Method

The existing padding oracle implementation was tested with plaintexts of different lengths. For each plaintext, the number of oracle queries was counted, and the recovered plaintext was compared with the original.

## Results

| Plaintext Length (bytes) | Ciphertext Blocks | Oracle Queries | Verified |
|---:|---:|---:|:---:|
| 0 | Fill from output | Fill from output | Fill from output |
| 2 | Fill from output | Fill from output | Fill from output |
| 5 | Fill from output | Fill from output | Fill from output |
| 15 | Fill from output | Fill from output | Fill from output |
| 16 | Fill from output | Fill from output | Fill from output |
| 17 | Fill from output | Fill from output | Fill from output |
| 32 | Fill from output | Fill from output | Fill from output |
| 38 | Fill from output | Fill from output | Fill from output |

## Observations

The number of oracle queries depends on the number of ciphertext blocks and the guesses needed to recover the plaintext bytes. Each byte is recovered by trying possible values and checking the oracle response.

PKCS#7 padding adds a complete block when the plaintext length is an exact multiple of the AES block size. Therefore, the number of ciphertext blocks does not always increase only when the plaintext length exceeds a multiple of 16.

## Conclusion

The experiment demonstrates that the Padding Oracle Attack can recover plaintext through repeated oracle queries. The query count depends on the plaintext length, block count, and number of guesses required during byte recovery.
