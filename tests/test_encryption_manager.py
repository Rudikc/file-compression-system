import os

import pytest

from encryption.encryption_manager import EncryptionManager


@pytest.fixture(scope="function")
def setup_encryption_manager():
    return EncryptionManager()


@pytest.mark.parametrize("data", [b"Sensitive data to encrypt", b""])
def test_encrypt_and_decrypt(setup_encryption_manager, data):
    manager = setup_encryption_manager
    password = b"StrongPassword123"

    encrypted_data = manager.encrypt(data, password)
    assert isinstance(encrypted_data, bytes)
    assert len(encrypted_data) > len(data)  # Encrypted data should contain salt and IV

    decrypted_data = manager.decrypt(encrypted_data, password)
    assert decrypted_data == data


def test_encrypt_with_large_data(setup_encryption_manager):
    manager = setup_encryption_manager
    data = os.urandom(10**8)
    password = b"StrongPassword123"

    encrypted_data = manager.encrypt(data, password)
    assert isinstance(encrypted_data, bytes)
    assert len(encrypted_data) > len(data)  # Encrypted data should contain salt and IV

    decrypted_data = manager.decrypt(encrypted_data, password)
    assert decrypted_data == data


def test_decrypt_with_wrong_password(setup_encryption_manager):
    manager = setup_encryption_manager
    data = b"Sensitive data to encrypt"
    password = b"StrongPassword123"
    wrong_password = b"WrongPassword456"

    encrypted_data = manager.encrypt(data, password)

    with pytest.raises(ValueError):
        manager.decrypt(encrypted_data, wrong_password)


def test_salt_and_iv_uniqueness(setup_encryption_manager):
    manager = setup_encryption_manager
    data = b"Test data for salt and IV uniqueness"
    password = b"StrongPassword123"

    encrypted_data_1 = manager.encrypt(data, password)
    encrypted_data_2 = manager.encrypt(data, password)

    assert encrypted_data_1 != encrypted_data_2


def test_invalid_data_format_during_decrypt(setup_encryption_manager):
    manager = setup_encryption_manager
    invalid_data = b"Invalid data not following encryption format"
    password = b"StrongPassword123"

    with pytest.raises(Exception):
        manager.decrypt(invalid_data, password)
