import os, json

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
FILE_PATH = os.path.join(BASE_DIR, "data", "orders.json")


def load_orders():
    """Lee las órdenes desde orders.json.

    Retorna:
        list: órdenes guardadas.
    """
    with open(FILE_PATH, "r", encoding="utf-8") as file:
        orders = json.load(file)
        return orders

def save_orders(orders):
    """Guarda las órdenes en orders.json.

    Parámetros:
        orders (list): órdenes a persistir.
    """
    with open(FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(orders, file, indent=4, ensure_ascii=False)
