from data import orders_data
from services import event_service


def create_order(newOrderData):
    if len(orders_data.orders) > 0:
        newOrderData["id"] = orders_data.orders[-1]["id"] + 1
    else:
        newOrderData["id"] = 1

    orders_data.orders.append(newOrderData)
    orders_data.save_orders()
    orders_data.write_order_log(newOrderData)

    return True, newOrderData


def get_orders_by_customer(customer_id):
    customer_orders = []

    for order in orders_data.orders:
        if order["customer_id"] == customer_id:
            customer_orders.append(order)

    return customer_orders

def restore_orders_availability():
    for order in orders_data.orders:
        event = event_service.get_event_by_id(order["event_id"])

        if event is None:
            continue

        if "event_name" not in order or "event_datetime" not in order:
            continue

        if event["name"] != order["event_name"]:
            continue

        if event["datetime"] != order["event_datetime"]:
            continue

        event_service.update_event_availability_service(
            order["event_id"],
            order["sector"],
            order["quantity"],
            order["seats"]
        )