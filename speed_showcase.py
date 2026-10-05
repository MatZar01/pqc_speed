#%%
import time
import oqs

def microseconds(start_ns):
    return (time.perf_counter_ns() - start_ns) / 1000


def test_kem(algorithm):
    print(f"\n--- KEM: {algorithm} ---")

    if algorithm not in oqs.get_enabled_kem_mechanisms():
        print("Not supported by this liboqs build")
        return

    # Receiver owns the private key
    with oqs.KeyEncapsulation(algorithm) as receiver, \
         oqs.KeyEncapsulation(algorithm) as sender:

        # 1. Generate key pair
        start = time.perf_counter_ns()
        public_key = receiver.generate_keypair()
        keygen_us = microseconds(start)

        # 2. Sender encapsulates a random shared secret
        start = time.perf_counter_ns()
        ciphertext, sender_secret = sender.encap_secret(public_key)
        encap_us = microseconds(start)

        # 3. Receiver recovers the same secret
        start = time.perf_counter_ns()
        receiver_secret = receiver.decap_secret(ciphertext)
        decap_us = microseconds(start)

        print(f"keygen: {keygen_us:10.2f} us")
        print(f"encap:  {encap_us:10.2f} us")
        print(f"decap:  {decap_us:10.2f} us")

        print(f"public key: {len(public_key):,} bytes")
        print(f"ciphertext: {len(ciphertext):,} bytes")
        print(f"shared secret: {len(sender_secret)} bytes")

        print("Same secret:", sender_secret == receiver_secret)


def test_signature(algorithm, sign_message, val_message):
    print(f"\n--- SIGNATURE: {algorithm} ---")

    if algorithm not in oqs.get_enabled_sig_mechanisms():
        print("Not supported by this liboqs build")
        return

    with oqs.Signature(algorithm) as signer, \
         oqs.Signature(algorithm) as verifier:

        # 1. Generate signing key pair
        public_key = signer.generate_keypair()

        # 2. Sign
        start = time.perf_counter_ns()
        signature = signer.sign(sign_message)
        sign_us = microseconds(start)

        # 3. Verify
        start = time.perf_counter_ns()
        valid = verifier.verify(val_message, signature, public_key)
        verify_us = microseconds(start)

        print(f"sign:   {sign_us:10.2f} us")
        print(f"verify: {verify_us:10.2f} us")

        print(f"public key: {len(public_key):,} bytes")
        print(f"signature:  {len(signature):,} bytes")

        print("Signature valid:", valid)


print("liboqs:", oqs.oqs_version())

test_kem("ML-KEM-512")
test_kem("Classic-McEliece-348864")

message = b"Welcome to the PQC seminar!"

test_signature("ML-DSA-44", sign_message=message, val_message=message)
test_signature("SLH_DSA_PURE_SHA2_128F", sign_message=message, val_message=message)

altered_message = b"Altered PQC seminar!"

test_signature("ML-DSA-44", sign_message=message, val_message=altered_message)
test_signature("SLH_DSA_PURE_SHA2_128F", sign_message=message, val_message=altered_message)
