from utils.password_helpers import hash_password, verify_password


def test_hash_password():
    password = "Clave123"

    hashed_password = hash_password(password)

    assert hashed_password != password
    assert len(hashed_password) == 64


def test_verify_password_correct():
    password = "Clave123"
    hashed_password = hash_password(password)

    result = verify_password(password, hashed_password)

    assert result == True


def test_verify_password_incorrect():
    password = "Clave123"
    hashed_password = hash_password(password)

    result = verify_password("OtraClave123", hashed_password)

    assert result == False