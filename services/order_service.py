from data import orders_data


def create_order(newOrderData):
    if len(orders_data.orders) > 0:
        newOrderData["id"] = orders_data.orders[-1]["id"] + 1
    else:
        newOrderData["id"] = 1

    orders_data.orders.append(newOrderData)

    return True, newOrderData


def get_orders_by_customer(customer_id):
    customer_orders = []

    for order in orders_data.orders:
        if order["customer_id"] == customer_id:
            customer_orders.append(order)

    return customer_orders