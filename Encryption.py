from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import os


# Function to derive a key from the password (fixed key length)
def derive_key(password, salt, key_length):
    iterations = 100000  # Fixed number of iterations

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=key_length,  # Key length: 16 for AES-128, 32 for AES-256
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    return kdf.derive(password.encode())


# Function to encrypt the password with a fixed key size
def encrypt_password(password):
    length = len(password)


    # Use AES-256 (32-byte key length)
    salt = os.urandom(16)  # Random salt
    key = derive_key(password, salt, 32)

    # Use AES encryption with CBC mode
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Padding password to match block size (16 bytes for AES)
    padded_password = password.ljust((len(password) + 15) // 16 * 16)
    ciphertext = encryptor.update(padded_password.encode()) + encryptor.finalize()

    return salt + iv + ciphertext


# Function to decrypt the password based on its original length
def decrypt_password(encrypted_password, password):
    # Extract salt and IV from the encrypted data
    salt = encrypted_password[:16]
    iv = encrypted_password[16:32]
    ciphertext = encrypted_password[32:]

    # Derive the same key used for encryption
    key = derive_key(password, salt, 32)

    # Decrypt with AES in CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()
    decrypted_password = decrypted_padded.decode().strip()  # Remove padding

    return decrypted_password


# Example usage
password = "ABCDE!32aBs"  # Example password with 12 characters
if len(password) < 8 or len(password) > 16:
    print("Password must be between 8 and 16 characters long")
else:
    #encrypt
    encrypted = encrypt_password(password)
    print("Encrypted password:", encrypted)
    #decrypt
    decrypted = decrypt_password(encrypted, password)
    print("Decrypted password:", decrypted)
