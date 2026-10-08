# CY2550 Project 2 — Answers
Note: completed on macOS; used `md5` and `shasum -a 256` in place of
`md5sum` and `sha256sum`.

## Part 1: Symmetric Encryption

### 1.1
<!-- PBKDF2 = key derivation function. Turns passphrase + salt into a
256-bit key. Iterates many times so each password guess is slow.
Needed because a passphrase isn't a key: wrong length, low entropy. -->

### 1.2
<!-- Each run picks a random salt (visible after "Salted__" in the file)
→ different key + IV → different ciphertext.
If identical: deterministic encryption. Attacker sees when the same
message is sent twice, and can confirm guessed plaintexts. -->

### 1.3
<!-- Q1: ECB = 3 distinct blocks (24 / 12 / 1, the 1 is padding).
CBC = 37 distinct, each once. Most common ECB block repeats 24 times.
Q2: ECB leaked structure: which plaintext blocks are equal, how many,
where. Worth: patterns in data (repeated DB values, image outlines,
known message layouts), without ever breaking AES.
Q3: "What mode of operation?" (plus: are IVs/nonces unique? is there
integrity protection?) -->

## Part 2: Integrity

### 2.2
<!-- SHA-256: no secret, so anyone can compute it. Attacker modifies the
file, recomputes the hash, replaces both. Colleague's check passes.
HMAC: needs a shared secret key. Attacker can still modify, drop, or
delay, but can't forge a valid tag for changed content → tampering is
detected.
Can/cannot: SHA-256: attacker CAN modify undetected. HMAC: attacker
CAN'T forge, but CAN block or replay. Neither gives confidentiality.
Key must be shared over a different channel. -->

## Part 3: Cryptographic Keys

### 3.3 Q1
<!-- Proves: whoever uploaded controls that inbox (at that moment).
Does NOT prove: real identity, that the name is true, that the inbox
wasn't compromised, or that the key is trustworthy. -->

### 3.3 Q2
<!-- Procedure: compare all 40 hex characters over an independent channel
the attacker doesn't control: in person, or a voice/video call where
you recognize them.
Why it works: the attacker can swap keys on the network, but can't make
a different key with the same fingerprint (hash collision/preimage
resistance), and can't impersonate the classmate out-of-band. -->

## Part 4: Asymmetric Encryption

### 4.2
<!-- Note: newer GPG shows an "ocb encrypted packet" (AES-256, OCB AEAD
mode) instead of a plain "encrypted data packet."
pubkey enc packet: random session key, encrypted with my RSA public
encryption subkey (keyid 7930137AAFB17D01).
encrypted packet: my message (compressed), encrypted with AES using
that session key.
Why: RSA is slow and limited to small inputs; AES is fast for any size.
Name: hybrid encryption. -->

### 4.3
<!-- Signing: my private key. Verifying: my public key.
Encryption: recipient's public key. Decryption: recipient's private key.
Property signing gives: authenticity / integrity / non-repudiation.
Optional: the first corruption at byte 200 didn't break the signature
(that byte didn't change or wasn't covered); re-signing changed the
bytes and the corruption then caused a failed verify. -->

## Part 5: SSH Keys
<!-- Used my existing Ed25519 key (already on GitHub) if that's what you did.
Two sentences: strength depends on the best known attack, not bit
length. Factoring (RSA) has sub-exponential attacks → needs huge keys.
Elliptic-curve discrete log has no comparable shortcut → ~256-bit
Ed25519 ≈ 128-bit security, comparable to or better than RSA-3072. -->

## Part 7: Grading the Machine

### 7.1
<!-- AI used: ____. Prompt: "Write me a Python function that encrypts a
file with AES." First response used verbatim. -->

### 7.2
<!-- Credit what it did right: AES-GCM (authenticated), random 12-byte
nonce from os.urandom, maintained library.
Defects (for each: what's wrong / attacker capability / concept):
1. No KDF: password used directly → fast offline brute force (key
   derivation, PBKDF2 from 1.1).
2. No salt → same password = same key across files; precomputation
   attacks (salting).
3. Zero-padding short passwords → real key space = password space, not
   2^256 (entropy / key space).
4. Truncation at 32 bytes → different long passwords sharing the first
   32 chars produce the same key.
5. (minor) No decrypt function → the GCM tag is never verified in this
   code; can't round-trip. -->

### 7.3
<!-- Changes → defect fixed:
scrypt KDF → defects 1, 3, 4.
Random 16-byte salt per file, stored in output → defect 2.
Decrypt function using AESGCM.decrypt → tag verified, tamper/wrong
password raises InvalidTag (defect 5).
Password from getpass, not hardcoded.
Demo: round trip passed diff; flipping a byte → InvalidTag
(screenshots in PDF). -->