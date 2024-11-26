from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
from cryptography.hazmat.backends import default_backend

from encryption.password import Password


class EncryptionManager:
    def __init__(self):
        self.backend = default_backend()
        self.block_size = 128

    def encrypt(self, data: bytes, password: Password):
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=self.backend,
        )
        key = kdf.derive(password.to_bytes())

        iv = os.urandom(16)

        padder = padding.PKCS7(self.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        return salt + iv + encrypted_data

    def decrypt(self, data: bytes, password: Password):
        salt = data[:16]
        iv = data[16:32]
        encrypted_data = data[32:]

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=self.backend,
        )
        key = kdf.derive(password.to_bytes())

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

        unpadder = padding.PKCS7(self.block_size).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()

        return data
