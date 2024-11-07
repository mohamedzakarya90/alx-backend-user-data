#!/usr/bin/env python3
""" returning salted and hashed password - byte in string """
import bcrypt


def hash_password(password: str) -> bytes:
    """ returning the byte string password """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ implementing is_valid to the validate provided password which
    matched the hashed_password
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
