from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
import base64


class DocumentEncryption:
    """Handles document encryption and decryption using AES-256"""
    
    def __init__(self, key: str):
        # Ensure key has exactly 32 bytes (256 bits)
        self.key = self._ensure_key_length(key)
    
    def _ensure_key_length(self, key: str) -> bytes:
        """Ensures key has exactly 32 bytes"""
        key_bytes = key.encode('utf-8')
        if len(key_bytes) < 32:
            # Pad with zeros if too short
            key_bytes = key_bytes.ljust(32, b'\0')
        elif len(key_bytes) > 32:
            # Truncate if too long
            key_bytes = key_bytes[:32]
        return key_bytes
    
    def encrypt(self, data: bytes) -> bytes:
        """
        Encrypts data using AES-256-CBC
        Returns: IV (16 bytes) + encrypted data
        """
        # Generate random IV
        iv = os.urandom(16)
        
        # Create cipher
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        
        # Apply PKCS7 padding
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()
        
        # Encrypt
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        
        # Return IV + encrypted data
        return iv + encrypted_data
    
    def decrypt(self, encrypted_data: bytes) -> bytes:
        """
        Decrypts data using AES-256-CBC
        Expects: IV (16 bytes) + encrypted data
        """
        # Extract IV (first 16 bytes)
        iv = encrypted_data[:16]
        ciphertext = encrypted_data[16:]
        
        # Create cipher
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        
        # Decrypt
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Remove padding
        unpadder = padding.PKCS7(128).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()
        
        return data
    
    def encrypt_file(self, file_content: bytes) -> bytes:
        """Encrypts file content"""
        return self.encrypt(file_content)
    
    def decrypt_file(self, encrypted_content: bytes) -> bytes:
        """Decrypts file content"""
        return self.decrypt(encrypted_content)

