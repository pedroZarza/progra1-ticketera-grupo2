import os, json

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
FILE_PATH = os.path.join(BASE_DIR, "data", "events.json")


def load_events():
    with open(FILE_PATH, "r", encoding="utf-8") as file:
        events = json.load(file)
        return events

def save_events(events):
    with open(FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(events, file, indent=4, ensure_ascii=False)