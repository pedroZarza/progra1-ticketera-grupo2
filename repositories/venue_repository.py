import os, json

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
FILE_PATH = os.path.join(BASE_DIR, "data", "venues.json")


def load_venues():
    """Lee los venues desde venues.json.

    Retorna:
        list: venues guardados.
    """
    with open(FILE_PATH, "r", encoding="utf-8") as file:
        venues = json.load(file)
        return venues

def save_venues(venues):
    """Guarda los venues en venues.json.

    Parámetros:
        venues (list): venues a persistir.
    """
    with open(FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(venues, file, indent=4, ensure_ascii=False)
