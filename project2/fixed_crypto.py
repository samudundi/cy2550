import os
import sys
import getpass
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

SALT_LEN = 16
NONCE_LEN = 12


def derive_key(password: bytes, salt: bytes) -> bytes:
    # Slow, salted key derivation: replaces truncate/zero-pad
    kdf = Scrypt(salt=salt, length=32, n=2**15, r=8, p=1)
    return kdf.derive(password)


def encrypt_file(input_file, output_file, password: bytes):
    salt = os.urandom(SALT_LEN)        # new random salt per file
    nonce = os.urandom(NONCE_LEN)      # new random nonce per file
    key = derive_key(password, salt)

    with open(input_file, "rb") as f:
        data = f.read()

    ciphertext = AESGCM(key).encrypt(nonce, data, None)

    with open(output_file, "wb") as f:
        f.write(salt + nonce + ciphertext)


def decrypt_file(input_file, output_file, password: bytes):
    with open(input_file, "rb") as f:
        blob = f.read()

    salt = blob[:SALT_LEN]
    nonce = blob[SALT_LEN:SALT_LEN + NONCE_LEN]
    ciphertext = blob[SALT_LEN + NONCE_LEN:]
    key = derive_key(password, salt)

    # Raises InvalidTag if the password is wrong or the file was tampered with
    plaintext = AESGCM(key).decrypt(nonce, ciphertext, None)

    with open(output_file, "wb") as f:
        f.write(plaintext)


if __name__ == "__main__":
    if len(sys.argv) != 4 or sys.argv[1] not in ("enc", "dec"):
        print("Usage: python3 fixed_crypto.py enc|dec <input> <output>")
        sys.exit(1)
    mode, inp, out = sys.argv[1:]
    pw = getpass.getpass("Password: ").encode()
    if mode == "enc":
        encrypt_file(inp, out, pw)
    else:
        decrypt_file(inp, out, pw)