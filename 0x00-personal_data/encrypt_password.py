#!/usr/bin/env python3
"""
Module for hashing and verifying passwords using bcrypt.
"""
import bcrypt
from bcrypt import hashpw


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The hashed password.
    """
    b = password.encode()
    hashed = hashpw(b, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Verifies a password against a given hashed password.

    Args:
        hashed_password (bytes): The stored hashed password.
        password (str): The password to validate.

    Returns:
        bool: True if the password matches
        the hashed password, False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
