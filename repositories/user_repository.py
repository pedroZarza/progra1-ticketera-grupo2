import os, json

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
FILE_PATH = os.path.join(BASE_DIR, "data", "users.json")


def load_users():
    """Lee los usuarios desde users.json.

    Retorna:
        list: usuarios guardados.
    """
    with open(FILE_PATH, "r", encoding="utf-8") as file:
        users = json.load(file)
        return users

def save_users(users):
    """Guarda los usuarios en users.json.

    Parámetros:
        users (list): usuarios a persistir.
    """
    with open(FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4, ensure_ascii=False)
