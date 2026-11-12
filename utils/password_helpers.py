import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def verify_password(password, stored_hash):
    return hash_password(password) == stored_hash