
import padding_oracle as attack
from Crypto.Util.Padding import unpad

messages = [
    b"",
    b"Hi",
    b"Hello",
    b"A" * 15,
    b"A" * 16,
    b"A" * 17,
    b"A" * 32,
    b"This is a longer message for testing."
]

print(f"{'Length':>8} {'Blocks':>8} {'Queries':>10} {'Verified':>10}")

for message in messages:
    key, iv, ciphertext = attack.encrypt_message(message)

    attack.oracle_key = key
    attack.oracle_queries = 0

    recovered = attack.padding_oracle_attack(iv, ciphertext)
    recovered = unpad(recovered, attack.BLOCK_SIZE)

    verified = recovered == message
    blocks = len(ciphertext) // attack.BLOCK_SIZE

    print(
        f"{len(message):8} {blocks:8} "
        f"{attack.oracle_queries:10} {str(verified):>10}"
    )
