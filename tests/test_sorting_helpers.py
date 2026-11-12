from utils.sorting_helpers import (
    selection_sort_by_name,
    bubble_sort_by_id,
    insertion_sort_by_datetime
)


def test_selection_sort_by_name():
    items = [
        {"name": "Teatro"},
        {"name": "Rock"},
        {"name": "Comedia"}
    ]

    result = selection_sort_by_name(items)

    assert result[0]["name"] == "Comedia"
    assert result[1]["name"] == "Rock"
    assert result[2]["name"] == "Teatro"


def test_bubble_sort_by_id():
    items = [
        {"id": 3},
        {"id": 1},
        {"id": 2}
    ]

    result = bubble_sort_by_id(items)

    assert result[0]["id"] == 1
    assert result[1]["id"] == 2
    assert result[2]["id"] == 3


def test_insertion_sort_by_datetime():
    items = [
        {"datetime": "2026-12-20T20:00"},
        {"datetime": "2026-12-10T20:00"},
        {"datetime": "2026-12-15T20:00"}
    ]

    result = insertion_sort_by_datetime(items)

    assert result[0]["datetime"] == "2026-12-10T20:00"
    assert result[1]["datetime"] == "2026-12-15T20:00"
    assert result[2]["datetime"] == "2026-12-20T20:00"