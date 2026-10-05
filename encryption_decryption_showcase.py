#%%
import os
import hashlib
import secrets

import oqs
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag


# --------------------------------------------------
# Demo option:
# False -> normal successful decryption
# True  -> corrupt receiver's shared secret
# --------------------------------------------------

ALTER_RECEIVER_SECRET = False


# --------------------------------------------------
# 1. Create some application data
# --------------------------------------------------

text = f"Sensor reading: {secrets.randbelow(1000)}"
plaintext = text.encode()

print("Original message:", text)


# --------------------------------------------------
# 2. Establish a shared secret using ML-KEM
# --------------------------------------------------

with oqs.KeyEncapsulation("ML-KEM-768") as receiver, \
     oqs.KeyEncapsulation("ML-KEM-768") as sender:

    # Receiver generates the KEM key pair
    public_key = receiver.generate_keypair()

    # Sender encapsulates a random shared secret
    kem_ciphertext, sender_secret = sender.encap_secret(public_key)

    # Receiver decapsulates and obtains the same secret
    receiver_secret = receiver.decap_secret(kem_ciphertext)


print("\nShared secrets equal:",
      sender_secret == receiver_secret)


# --------------------------------------------------
# 3. Optionally corrupt receiver's secret
# --------------------------------------------------

if ALTER_RECEIVER_SECRET:

    print("\n*** ALTERING RECEIVER SECRET ***")

    # Convert immutable bytes into mutable bytearray
    altered_secret = bytearray(receiver_secret)

    # Flip one bit in the first byte
    altered_secret[0] ^= 0x01

    # Convert back to bytes
    receiver_secret = bytes(altered_secret)


print("Shared secrets equal after alteration:",
      sender_secret == receiver_secret)


# --------------------------------------------------
# 4. Derive AES-256 keys
# --------------------------------------------------

sender_key = hashlib.sha256(sender_secret).digest()
receiver_key = hashlib.sha256(receiver_secret).digest()

print("AES keys equal:",
      sender_key == receiver_key)


# --------------------------------------------------
# 5. Sender encrypts the message using AES-GCM
# --------------------------------------------------

nonce = os.urandom(12)

aes_sender = AESGCM(sender_key)

encrypted = aes_sender.encrypt(
    nonce,
    plaintext,
    None
)

print("\nEncrypted message:")
print(encrypted.hex())


# --------------------------------------------------
# 6. Receiver attempts to decrypt
# --------------------------------------------------

aes_receiver = AESGCM(receiver_key)

try:

    decrypted = aes_receiver.decrypt(
        nonce,
        encrypted,
        None
    )

    print("\nDecryption successful!")
    print("Decrypted message:", decrypted.decode())

except InvalidTag:

    print("\nDECRYPTION FAILED")
    print("Receiver has the wrong key.")
    print("AES-GCM authentication detected the mismatch.")