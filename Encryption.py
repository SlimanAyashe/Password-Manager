from cryptography.fernet import Fernet
import base64
import hashlib


# Generate a key for encryption and decryption
def generate_key_from_number(number: int) -> bytes:
    # Convert the number to a string and hash it
    number_str = str(number).encode()  # Convert number to bytes
    hashed = hashlib.sha256(number_str).digest()  # Hash the bytes using SHA-256

    # Encode the hash to a base64 URL-safe string
    key = base64.urlsafe_b64encode(hashed[:32])  # Use the first 32 bytes
    return key


def encrypt_message(message: str) -> bytes:
    """Encrypts a message using Fernet symmetric encryption."""
    # Generate the key based on the original message length
    cipher = Fernet(generate_key_from_number(len(message)))
    print(cipher)
    message_bytes = message.encode()  # Convert the message to bytes
    encrypted_message = cipher.encrypt(message_bytes)  # Encrypt the message

    # Calculate the index to indicate the length of the original string modulo 9
    length_indicator = len(message) -8
    # Append the length indicator as a byte
    encrypted_message += bytes([length_indicator])
    return encrypted_message


def decrypt_message(encrypted_message: bytes) -> str:
    """Decrypts an encrypted message using Fernet symmetric encryption."""
    # Get the length indicator from the last byte of the encrypted message
    length_indicator = encrypted_message[-1]

    # Generate the key based on the original message length
    cipher = Fernet(generate_key_from_number(length_indicator+8))

    # Remove the length indicator from the encrypted message
    new_string = encrypted_message[:-1]

    # Decrypt the message
    decrypted_message = cipher.decrypt(new_string)  # Decrypt the message
    return decrypted_message.decode()  # Convert bytes back to string


# Example usage
if __name__ == "__main__":
    while True:
        msg=input("Enter password of length 8-16\n")
        if len(msg)<8 or len(msg)>16:
            print("invalid length!")
        else:
            # Encrypt the message
            encrypted = encrypt_message(msg)
            print("Encrypted Message:", encrypted)

            # Decrypt the message
            decrypted = decrypt_message(encrypted)
            print("Decrypted Message:", decrypted)
