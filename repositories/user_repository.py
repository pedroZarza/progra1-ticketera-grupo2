import os, json

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
FILE_PATH = os.path.join(BASE_DIR, "data", "users.json")


def load_users():
    with open(FILE_PATH, "r", encoding="utf-8") as file:
        users = json.load(file)
        return users

def save_users(users):
    with open(FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4, ensure_ascii=False)
