# PQC Speed Showcase

Small Python demos for exploring post-quantum cryptography with
[liboqs](https://github.com/open-quantum-safe/liboqs) and its Python bindings.

The repository is a seminar demonstrations only. It shows how key encapsulation mechanisms, digital signatures,
and hybrid post-quantum plus symmetric encryption behave in practice.

## Contents

- `speed_showcase.py` benchmarks selected post-quantum algorithms and prints
  operation timings, key sizes, ciphertext or signature sizes, and validation
  results.
- `encryption_decryption_showcase.py` uses ML-KEM to establish a shared secret,
  derives AES-256 keys with SHA-256, then encrypts and decrypts a sample sensor
  reading with AES-GCM.
- `liboqs_install.sh` builds and installs the native `liboqs` library into the
  active Conda environment.

## Requirements

- Python 3.10+
- Conda environment recommended
- CMake, Git, and a C/C++ build toolchain
- Native `liboqs`
- Python packages:
  - `liboqs-python`
  - `cryptography`

## Setup

Create and activate a Conda environment:

```bash
conda create -n pqc-speed python=3.11 cmake git pip -c conda-forge
conda activate pqc-speed
```

Build and install `liboqs` into that environment:

```bash
bash liboqs_install.sh
```

Install the Python dependencies:

```bash
pip install liboqs-python cryptography
```

The install script expects `CONDA_PREFIX` to be set, so run it only after
activating the environment.

## Usage

Run the speed and size demo:

```bash
python speed_showcase.py
```

This script currently exercises:

- `ML-KEM-512`
- `Classic-McEliece-348864`
- `ML-DSA-44`
- `SLH_DSA_PURE_SHA2_128F`

For KEMs, it prints key generation, encapsulation, and decapsulation timings in
microseconds, along with public key, ciphertext, and shared-secret sizes. For
signatures, it prints signing and verification timings, public key and signature
sizes, and whether verification succeeded.

The signature demo signs one message and verifies both the original message and
an altered message, so the altered-message checks should report invalid
signatures.

Run the encryption and decryption demo:

```bash
python encryption_decryption_showcase.py
```

This script:

1. Creates a random sample sensor reading.
2. Establishes a shared secret with `ML-KEM-768`.
3. Derives matching AES-256 keys from the shared secret.
4. Encrypts the message with AES-GCM.
5. Decrypts it and prints the recovered plaintext.

To demonstrate authenticated decryption failure, set this flag in
`encryption_decryption_showcase.py`:

```python
ALTER_RECEIVER_SECRET = True
```

With the receiver secret altered, the AES-GCM authentication check should fail
and the script should print `DECRYPTION FAILED`.

## Notes

- Algorithm availability depends on how `liboqs` was built. If an algorithm is
  missing from the local build, `speed_showcase.py` prints a "Not supported"
  message instead of running that test.
- Timings are simple single-run measurements intended for demonstration. 
- The AES key derivation in the encryption demo is intentionally simple for
  readability. 
