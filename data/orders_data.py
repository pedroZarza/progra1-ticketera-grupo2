import json


ORDERS_FILE = "data/orders.json"
LOG_FILE = "data/orders_log.txt"


def load_orders():
    try:
        with open(ORDERS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_orders():
    with open(ORDERS_FILE, "w", encoding="utf-8") as file:
        json.dump(orders, file, indent=4)


def write_order_log(order):
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(
            f"Orden #{order['id']} | "
            f"Cliente: {order['customer_id']} | "
            f"Evento: {order['event_id']} | "
            f"Sector: {order['sector']} | "
            f"Cantidad: {order['quantity']} | "
            f"Total: ${order['total']} | "
            f"Fecha: {order['purchase_date']}\n"
        )


orders = load_orders()