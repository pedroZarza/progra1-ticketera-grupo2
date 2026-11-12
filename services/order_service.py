from repositories import orders_repository, event_repository
from datetime import datetime


def create_order(newOrderData):
    orders = orders_repository.load_orders()
    events = event_repository.load_events()

    event = None

    for storedEvent in events:
        if storedEvent["id"] == newOrderData["event_id"]:
            event = storedEvent
            break

    if event is None:
        raise LookupError(
            f"No existe un evento con id '{newOrderData['event_id']}'"
        )

    if event["status"] != "active":
        raise ValueError("El evento seleccionado no está activo.")

    eventDate = datetime.fromisoformat(event["datetime"])

    if eventDate <= datetime.now():
        raise ValueError("El evento seleccionado ya finalizó.")

    sectorName = newOrderData["sector"]

    if sectorName not in event["sectors"]:
        raise ValueError("El sector seleccionado no existe.")

    sector = event["sectors"][sectorName]

    if sector["price"] is None:
        raise ValueError(
            "El sector seleccionado no tiene precio definido."
        )

    quantity = newOrderData["quantity"]

    if quantity <= 0:
        raise ValueError(
            "La cantidad de entradas debe ser mayor a cero."
        )

    selectedSeats = newOrderData["seats"]

    if "capacity" in sector:
        available = sector["capacity"] - sector["sold"]

        if quantity > available:
            raise ValueError(
                f"No hay suficientes entradas disponibles. "
                f"Disponibles: {available}")

        sector["sold"] += quantity

    elif "seats" in sector:

        if len(selectedSeats) != quantity:
            raise ValueError("La cantidad de butacas seleccionadas no coincide con la cantidad de entradas.")

        for seat in selectedSeats:
            row = seat[0]
            column = seat[1]

            if row < 0 or row >= len(sector["seats"]):
                raise ValueError("La fila seleccionada no existe.")

            if column < 0 or column >= len(sector["seats"][row]):
                raise ValueError("La butaca seleccionada no existe.")

            if sector["seats"][row][column] != "free":
                raise ValueError("Una de las butacas seleccionadas ya está ocupada.")

        for seat in selectedSeats:
            row = seat[0]
            column = seat[1]

            sector["seats"][row][column] = "occupied"

    else:
        raise ValueError("El sector seleccionado tiene una configuración inválida.")

    if len(orders) > 0:
        newOrderData["id"] = max(
            order["id"] for order in orders) + 1
    else:
        newOrderData["id"] = 1

    orders.append(newOrderData)

    event_repository.save_events(events)
    orders_repository.save_orders(orders)

    return newOrderData


def get_orders_by_customer(customer_id):
    orders = orders_repository.load_orders()
    customerOrders = []

    for order in orders:
        if order["customer_id"] == customer_id:
            customerOrders.append(order)

    return customerOrders