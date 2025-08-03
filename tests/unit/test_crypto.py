# tests/unit/test_crypto.py

import pytest
from src.utils.crypto import encrypt, decrypt

def test_encryption_decryption():
    message = "secure message"
    key = "testkey"
    encrypted = encrypt(message, key)
    decrypted = decrypt(encrypted, key)
    assert decrypted == message
