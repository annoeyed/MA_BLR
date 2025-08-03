"""
Unit tests for cryptographic utility functions.
"""
import pytest
from src.utils.crypto import sha256, hmac_sha256, rand_token

def test_sha256():
    """
    Tests the sha256 hashing function.
    """
    assert sha256("hello") == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
    assert sha256("") == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

def test_hmac_sha256():
    """
    Tests the HMAC-SHA256 function.
    """
    key = "secret"
    message = "hello"
    # Known value for HMAC-SHA256 with key 'secret' and message 'hello'
    expected = "926a8d3e21a224a3c215352c525f0aab5c425e1975b72ff2a2a07849c4033e06"
    assert hmac_sha256(key, message) == expected

def test_rand_token():
    """
    Tests the random token generation.
    """
    token1 = rand_token(16)
    token2 = rand_token(16)
    assert isinstance(token1, str)
    assert len(token1) == 32 # 16 bytes = 32 hex characters
    assert token1 != token2
