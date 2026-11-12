from services.event_service import has_availability
from utils.layout_helpers import count_sold_seats
from utils.password_helpers import hash_password, verify_password


# hash_password

def test_hash_password():
    password = "Clave123"
    hashed_password = hash_password(password)
    assert hashed_password != password
    assert len(hashed_password) == 64


def test_hash_password_is_deterministic():
    password = "Clave123"
    assert hash_password(password) == hash_password(password)


def test_hash_password_differs_by_case():
    assert hash_password("Clave123") != hash_password("clave123")


def test_hash_password_empty():
    hashed_password = hash_password("")
    assert hashed_password != ""
    assert len(hashed_password) == 64


# verify_password

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


def test_verify_password_rejects_different_case():
    hashed_password = hash_password("Clave123")
    result = verify_password("clave123", hashed_password)
    assert result == False


def test_verify_password_empty_matches_only_itself():
    hashed_password = hash_password("")
    assert verify_password("", hashed_password) == True
    assert verify_password("Clave123", hashed_password) == False


# has_availability

def test_has_availability_when_general_sector_has_room():
    event = {
        "sectors": {
            "Campo": {"capacity": 100, "sold": 40}
        }
    }

    result = has_availability(event)

    assert result == True


def test_has_availability_when_general_sector_is_sold_out():
    event = {
        "sectors": {
            "Campo": {"capacity": 100, "sold": 100}
        }
    }

    result = has_availability(event)

    assert result == False


def test_has_availability_when_another_sector_has_a_free_seat():
    event = {
        "sectors": {
            "Campo": {"capacity": 100, "sold": 100},
            "Platea": {"seats": [["occupied", "free"], ["occupied", "occupied"]]}
        }
    }

    result = has_availability(event)

    assert result == True


def test_has_availability_when_every_seat_is_occupied():
    event = {
        "sectors": {
            "Platea": {"seats": [["occupied", "occupied"], ["occupied", "occupied"]]}
        }
    }

    result = has_availability(event)

    assert result == False


def test_has_availability_when_event_has_no_sectors():
    event = {"sectors": {}}

    result = has_availability(event)

    assert result == False


def test_has_availability_when_one_general_sector_has_one_ticket_left():
    event = {
        "sectors": {
            "Campo": {"capacity": 100, "sold": 100},
            "Platea": {"capacity": 50, "sold": 49}
        }
    }

    result = has_availability(event)

    assert result == True


def test_has_availability_when_numbered_sector_has_one_free_seat():
    event = {
        "sectors": {
            "Platea": {"seats": [["occupied"], ["free"]]}
        }
    }

    result = has_availability(event)

    assert result == True


def test_has_availability_when_numbered_sector_has_no_rows():
    event = {
        "sectors": {
            "Platea": {"seats": []}
        }
    }

    result = has_availability(event)

    assert result == False


def test_has_availability_when_sector_has_no_capacity_or_seats():
    event = {
        "sectors": {
            "Vip": {"price": 1000}
        }
    }

    result = has_availability(event)

    assert result == False


# count_sold_seats

def test_count_sold_seats():
    row = ["occupied", "free", "occupied", "occupied"]

    result = count_sold_seats(row)

    assert result == 3


def test_count_sold_seats_empty_row():
    result = count_sold_seats([])

    assert result == 0


def test_count_sold_seats_all_free():
    result = count_sold_seats(["free", "free", "free"])

    assert result == 0


def test_count_sold_seats_all_occupied():
    row = ["occupied", "occupied", "occupied"]

    result = count_sold_seats(row)

    assert result == len(row)


def test_count_sold_seats_ignores_other_statuses():
    row = ["occupied", "reserved", "free", "occupied"]

    result = count_sold_seats(row)

    assert result == 2





