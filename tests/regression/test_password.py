import pytest

from encryption.password import Password


def test_password_valid():
    password = Password("secure123")
    assert password.value == "secure123"
    assert password.to_bytes() == b"secure123"
    assert str(password) == "*********"


def test_password_minimum_length():
    with pytest.raises(ValueError, match="Password must be at least 6 characters long"):
        Password("short")


def test_password_empty():
    with pytest.raises(ValueError, match="Password must be at least 6 characters long"):
        Password("")


def test_password_to_bytes():
    password = Password("secure123")
    assert password.to_bytes() == b"secure123"


def test_password_masking():
    password = Password("secure123")
    assert str(password) == "*********"


def test_password_boundary_condition():
    password = Password("123456")
    assert password.value == "123456"
