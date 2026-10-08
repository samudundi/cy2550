# CY2550 Project 2 — Answers

**Note:** I completed the project on macOS, so I used `md5` and `shasum -a 256` instead of `md5sum` and `sha256sum`.

## Part 1: Symmetric Encryption

### 1.1

PBKDF2 is a key derivation function that takes a passphrase and a salt and turns them into a 256-bit encryption key. It is needed because a passphrase is not necessarily the correct length or strong enough to use directly as an encryption key, and PBKDF2 makes password guessing slower by performing many iterations.

### 1.2

Each time the encryption is run, a random salt is generated, which results in a different derived key and IV and therefore different ciphertext. If the same ciphertext were produced every time, an attacker could tell when the same message was encrypted more than once and could potentially confirm guesses about the plaintext.

### 1.3

**Q1:** With ECB, there were 3 distinct blocks: one repeated 24 times, one repeated 12 times, and one padding block. **The most common ECB block repeated 24 times.** With CBC, there were 37 distinct blocks, and each block appeared only once.

**Q2:** ECB leaks information about the structure of the plaintext because identical plaintext blocks produce identical ciphertext blocks. An attacker could therefore see repeated patterns, such as repeated database values, image outlines, or repeated parts of a message, without actually decrypting the data.

**Q3:** One important question to ask is what mode of operation is being used. It is also important to ask whether the IVs or nonces are unique and whether the encryption provides integrity protection.

## Part 2: Integrity

### 2.2

SHA-256 by itself does not provide protection against an attacker who can modify the file because the hash is not secret. An attacker could change the file, calculate a new SHA-256 hash, and replace the original hash, causing the colleague's check to pass.

HMAC uses a shared secret key, so an attacker who does not have the key cannot create a valid tag for modified content. An attacker can still block, delay, or replay a message, but they cannot forge a valid HMAC for changed content without the secret key.

The HMAC key must be shared through a separate secure channel. If the key were sent over the same channel controlled by the attacker, the attacker could obtain the key and recompute the HMAC after modifying the file.

Neither SHA-256 nor HMAC provides confidentiality. SHA-256 allows an attacker to modify the file without detection if they can replace the hash, while HMAC provides tamper detection as long as the secret key remains secure.

## Part 3: Cryptographic Keys

### 3.3 Q1

The email proves that whoever uploaded the public key has control of that email inbox at that time. However, it does not prove that the uploader is really the person named on the key, that the account has not been compromised, or that the public key itself is trustworthy.

### 3.3 Q2

I would compare the entire 40-character fingerprint with my classmate over an independent channel, such as in person or through a voice or video call where I can verify that I am actually speaking with them. This works because an attacker could replace the public key over the network, but they cannot easily create a different key with the same fingerprint or impersonate the classmate through an independent communication channel.

## Part 4: Asymmetric Encryption

### 4.2

The newer version of GPG showed an OCB encrypted packet using AES-256 instead of a plain encrypted data packet. The public-key encrypted packet contains a randomly generated session key encrypted with my RSA public encryption subkey, while the encrypted packet contains my compressed message encrypted with AES using that session key.

This is called **hybrid encryption** because RSA is used to securely encrypt the session key while AES is used to encrypt the actual message. RSA is slower and can only encrypt relatively small amounts of data, while AES is much faster and can efficiently encrypt data of any practical size.

### 4.3

For signing, I use my private key, and someone else uses my public key to verify the signature. For encryption, the recipient's public key is used to encrypt the message, and the recipient's private key is used to decrypt it.

Digital signatures provide authenticity and integrity, and they can also provide non-repudiation. In my test, the first corruption at byte 200 did not cause the signature verification to fail because that particular byte was either unchanged or was not part of the data covered by the signature; after re-signing, the corruption caused verification to fail.

## Part 5: SSH Keys

I used my existing Ed25519 SSH key, which was already connected to my GitHub account. The strength of a cryptographic key depends on the best known attack against the underlying algorithm, rather than simply the number of bits in the key; RSA relies on factoring, while Ed25519 relies on the elliptic-curve discrete logarithm problem, so a 256-bit Ed25519 key provides roughly 128 bits of security and is comparable to or stronger than RSA-3072.

## Part 7: Grading the Machine

### 7.1

I used ChatGPT for the AI-generated solution. My prompt was: **"Write me a Python function that encrypts a file with AES."** I used the first response without making changes to the original AI-generated code.

### 7.2

The code did some things correctly, including using AES-GCM, which provides authenticated encryption, and generating a random 12-byte nonce with `os.urandom`. It also used a standard cryptographic library instead of implementing AES itself.

**Defect 1: No key derivation function**

* **What's wrong:** The password is used directly as the encryption key instead of being passed through a key derivation function.
* **What an attacker could do:** If an attacker steals an encrypted file, they could try a very large number of password guesses offline because there is no expensive key derivation step slowing them down.
* **Concept violated:** **Key derivation / password-based keys.**

**Defect 2: No salt**

* **What's wrong:** The program does not generate a random salt when deriving the key from the password.
* **What an attacker could do:** The same password would produce the same key across different files, allowing attackers to identify repeated keys and use precomputed password guesses more efficiently.
* **Concept violated:** **Salting.**

**Defect 3: Zero-padding short passwords**

* **What's wrong:** Short passwords are padded with zeros to reach the required key length instead of being securely transformed into a high-entropy key.
* **What an attacker could do:** An attacker could focus on guessing the original password rather than searching the entire 256-bit key space, making brute-force attacks much easier.
* **Concept violated:** **Key space and entropy.**

**Defect 4: Truncating passwords longer than 32 bytes**

* **What's wrong:** Passwords longer than 32 bytes are cut down to their first 32 bytes.
* **What an attacker could do:** Two different long passwords that share the same first 32 bytes would produce the exact same encryption key, so the additional password characters provide no security.
* **Concept violated:** **Key space and entropy / proper key derivation.**

**Defect 5: No decryption function**

* **What's wrong:** The code only encrypts files and does not include a function that decrypts them and verifies the GCM authentication tag.
* **What an attacker could do:** The program cannot demonstrate that a modified ciphertext or incorrect password will be detected because the authentication tag is never checked by a decryption operation.
* **Concept violated:** **Authenticated encryption / integrity verification.**

### 7.3

**1. scrypt KDF:**
I replaced the password-to-key step with the scrypt key derivation function, which makes password guessing much slower and prevents attackers from directly using the password as an AES key. scrypt is also memory-hard, which makes cracking with GPUs or custom hardware more expensive. This also fixes the zero-padding and 32-byte truncation problems because scrypt properly derives a fixed-length key from the full password. (Fixes defects 1, 3, and 4 from 7.2.)

**2. Random salt:**
I added a random 16-byte salt for each encrypted file and stored the salt with the ciphertext so it can be used again during decryption. The salt does not need to be secret, so storing it in the file is safe. This prevents the same password from producing the same derived key across different files and makes precomputed attacks much harder. (Fixes defect 2.)

**3. Decryption and authentication:**
I added a decryption function using `AESGCM.decrypt()`, which verifies the authentication tag before returning the plaintext. If the password is wrong or the encrypted file has been modified, decryption raises an `InvalidTag` error before any output file is written, so tampered data never reaches disk. (Fixes defect 5.)

**4. Password input:**
The original function took the password as an argument but had no way of obtaining it. I added `getpass` so the program prompts for the password without echoing it on screen, and so it never appears in shell history or the process list the way a command-line argument would. This is a usability and safety improvement rather than a fix for one of the defects in 7.2.

**5. Testing:**
I tested the program by encrypting and then decrypting a file and confirmed that the decrypted file matched the original. I also flipped a byte in the encrypted file, which caused decryption to fail with `InvalidTag`, showing that the authentication check detects tampering. Screenshots of both tests are in the PDF.