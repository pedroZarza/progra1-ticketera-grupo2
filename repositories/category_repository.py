import json
import os

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
FILE_PATH = os.path.join(BASE_DIR, "data", "categories.json")


def load_categories():
    """Lee las categorías desde categories.json.

    Retorna:
        list: categorías guardadas.
    """
    with open(FILE_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def save_categories(categories):
    """Guarda las categorías en categories.json.

    Parameters:
        categories (list): categorías a persistir.
    """
    with open(FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(categories, file, indent=4, ensure_ascii=False)
