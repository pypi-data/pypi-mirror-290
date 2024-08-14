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
    """Derive the decryption key using PBKDF2 and hashlib."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),  # Using SHA-256 for stronger security
        length=KEY_LEN,
        salt=salt,
        iterations=ITERATIONS,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())
    return key

def decrypt_text(encrypted_data: str, password: str) -> str:
    """Decrypt the base64 encoded encrypted data using the given password."""
    # Decode the base64 encoded data
    encrypted_data_bytes = base64.b64decode(encrypted_data)
    
    # Extract salt, IV, encrypted text, and hash
    salt = encrypted_data_bytes[:SALT_LEN]
    iv = encrypted_data_bytes[SALT_LEN:SALT_LEN + IV_LEN]
    encrypted_text = encrypted_data_bytes[SALT_LEN + IV_LEN:-32]  # Last 32 bytes are the hash
    encrypted_text_hash = encrypted_data_bytes[-32:]
    
    # Derive the key from the password and salt
    key = derive_key(password, salt)
    
    # Initialize cipher for decryption
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    # Decrypt the data
    decrypted_padded_text = decryptor.update(encrypted_text) + decryptor.finalize()
    
    # Unpad the decrypted text
    pad_len = decrypted_padded_text[-1]
    decrypted_text = decrypted_padded_text[:-pad_len]
    
    # Verify the hash of the decrypted text
    if hashlib.sha256(encrypted_text).digest() != encrypted_text_hash:
        raise ValueError("Decryption failed: Integrity check failed.")
    
    return decrypted_text.decode('utf-8')

if __name__ == "__main__":
    encrypted_data = input("Enter the encrypted text (in base64): ").strip()
    password = input("Enter the password: ").strip()

    try:
        decrypted_text = decrypt_text(encrypted_data, password)
        print("Decrypted text:")
        print(decrypted_text)
    except Exception as e:
        print(f"Decryption failed: {e}")
