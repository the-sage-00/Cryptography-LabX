# Vigenere Cipher Cryptanalysis

## Aim

To perform cryptanalysis of a Vigenere cipher using Kasiski Examination and Frequency Analysis.

## Objectives

1. Preprocess the ciphertext.
2. Estimate the key length using Kasiski Examination.
3. Divide the ciphertext into groups according to the key length.
4. Perform frequency analysis on each group.
5. Determine the probable key.
6. Decrypt the ciphertext.
7. Verify the result by re-encryption.

## Techniques Used

### Kasiski Examination

Repeated sequences in the ciphertext are identified. The distances between their occurrences are calculated and factors of these distances are used to estimate possible key lengths.

### Index of Coincidence

The Index of Coincidence is calculated for each group to measure how closely the letter distribution resembles natural English text.

### Frequency Analysis

Each group is treated as a Caesar cipher. Letter frequencies are compared with standard English frequencies to estimate the Caesar shift.

### Vigenere Decryption

The recovered key is used to decrypt the ciphertext.

### Verification

The recovered plaintext is encrypted again using the recovered key. The resulting ciphertext is compared with the original ciphertext.

## User-Defined Functions

- clean_ciphertext()
- find_repeated_patterns()
- calculate_distances()
- find_factors()
- kasiski_analysis()
- calculate_ic()
- split_into_groups()
- frequency_analysis()
- find_shift()
- find_key()
- vigenere_decrypt()
- vigenere_encrypt()
- verify()

## Result

The program estimates the Vigenere key length, performs frequency analysis, recovers the probable key, decrypts the ciphertext and verifies the result using re-encryption.

## Cryptanalysis Process

The ciphertext is first cleaned by removing spaces and special characters.

Kasiski Examination is then performed to identify repeated patterns and calculate their distances. Factors of these distances provide candidate key lengths.

Since Kasiski Examination may produce multiple possible key lengths, Index of Coincidence is calculated for each candidate. The candidate whose average IC is closest to the expected English IC is selected as the probable key length.

The ciphertext is divided into groups according to the selected key length. Frequency analysis is then performed on each group. Each group is treated as a Caesar cipher and the probable shift is calculated using English letter frequencies.

The shifts are combined to obtain the probable Vigenere key. The recovered key is used to decrypt the ciphertext.

Finally, the recovered plaintext is encrypted again using the recovered key. The result is compared with the original ciphertext to verify the cryptanalysis.
