import hashlib
import uuid


def digest_string(string: str) -> str:
    salt = uuid.uuid1().hex
    hashed_string = hashlib.sha256(string.encode() + salt.encode()).hexdigest()
    return f"{hashed_string}:{salt}"


def check_digest(string: str, hashed_str: str) -> bool:
    password, salt = hashed_str.split(":")
    return password == hashlib.sha256(string.encode() + salt.encode()).hexdigest()
