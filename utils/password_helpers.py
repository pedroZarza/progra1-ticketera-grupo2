import hashlib

def hash_password(password):
    """Devuelve el hash SHA-256 de una contraseña.

    Parámetros:
        password (str): contraseña en texto plano.

    Retorna:
        str: hash hexadecimal.
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def verify_password(password, stored_hash):
    """Compara una contraseña con su hash almacenado.

    Parámetros:
        password (str): contraseña en texto plano.
        stored_hash (str): hash guardado.

    Retorna:
        bool: True si coinciden.
    """
    return hash_password(password) == stored_hash