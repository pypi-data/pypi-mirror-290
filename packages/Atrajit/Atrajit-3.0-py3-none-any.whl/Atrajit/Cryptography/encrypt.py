import os
import base64
import hashlib
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Constants
SALT_LEN = 64
KEY_LEN = 32
IV_LEN = 16
ITERATIONS = 100000

def derive_key(password: str, salt: bytes) -> bytes:
    """Derive the encryption key using PBKDF2 and hashlib."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),  # Using SHA-256 for stronger security
        length=KEY_LEN,
        salt=salt,
        iterations=ITERATIONS,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())
    return key

def encrypt_text(plain_text: str, password: str) -> str:
    """Encrypt the plain text using AES-256-CBC."""
    salt = os.urandom(SALT_LEN)
    key = derive_key(password, salt)
    iv = os.urandom(IV_LEN)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad the plain text
    pad_len = IV_LEN - len(plain_text) % IV_LEN
    padded_plain_text = plain_text + (chr(pad_len) * pad_len)
    
    encrypted_text = encryptor.update(padded_plain_text.encode('utf-8')) + encryptor.finalize()
    
    # Hash the encrypted text to verify integrity (optional)
    encrypted_text_hash = hashlib.sha256(encrypted_text).digest()
    
    # Combine salt, IV, encrypted text, and its hash, then encode with base64
    encrypted_data = base64.b64encode(salt + iv + encrypted_text + encrypted_text_hash).decode('utf-8')
    
    return encrypted_data

if __name__ == "__main__":
    plain_text = input("Enter the text to encrypt: ").strip()
    password = input("Enter the password: ").strip()

    encrypted_text = encrypt_text(plain_text, password)
    print(f"Encrypted text (in base64): {encrypted_text}")
