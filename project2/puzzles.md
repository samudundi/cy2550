# Puzzle 1 (CyberChef)

**Plaintext:** I got a jar of dirt

**Operation chain (applied in this order):**
1. Vigenère — Decode — key: `dirt`
2. Substitute — Decode direction: QWERTY keyboard order → standard alphabet
   (Plaintext field: QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm,
   Ciphertext field: ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz)
3. Base64 — Decode (From Base64)
4. Binary — Decode (From Binary, space delimiter, 8-bit bytes)

# Puzzle 2 (dCode)

**Plaintext:** NOT ALL TREASURES SILVER AND GOLD MATE

1. Scytale (transposition) — Decrypt — 5 turns of the band, spaces kept
2. Monoalphabetic substitution — Decode — letters → keypad digits
   (C→0, E→3, R→4, I→5, S→6, F→7, U→8, N→9). Key deduced: C always
   isolated (word separator = 0); group lengths constrain the digits.
3. Multi-tap Phone (SMS) — MLG ZOO GIVZHFIVH HROEVI ZMW TLOW NZGV
4. Atbash — NOT ALL TREASURES SILVER AND GOLD MATE

