from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os


def encrypt_file(input_file, output_file, password):
    # Derive a 256-bit AES key from the password
    key = password[:32].ljust(32, b"\0")

    # Generate a random 12-byte nonce
    nonce = os.urandom(12)

    # Read the file
    with open(input_file, "rb") as f:
        data = f.read()

    # Encrypt
    aesgcm = AESGCM(key)
    encrypted_data = aesgcm.encrypt(nonce, data, None)

    # Store nonce + encrypted data
    with open(output_file, "wb") as f:
        f.write(nonce)
        f.write(encrypted_data)
