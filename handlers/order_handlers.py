from utils import input_helpers, layout_helpers
from services import event_service, order_service
from utils.messages import show_error, show_success, show_info
from datetime import datetime


def buy_tickets(user):
    events = event_service.get_active_events()
    if len(events) == 0:
        show_info("No hay eventos disponibles.")
        return

    layout_helpers.events_board(events)

    eventId = input_helpers.prompt_positive_number("\nIngrese el ID del evento: ")
    if eventId == "q":
        return

    try:
        event = event_service.get_event_by_id(eventId)
    except LookupError as error:
        show_error(f"{error}")
        return

    eventDatetime = datetime.fromisoformat(event["datetime"])
    formattedDatetime = eventDatetime.strftime("%d/%m/%Y %H:%M")

    print(f"\nSELECCIÓN DE SECTOR | {event['name']} - {formattedDatetime}")
    print(event["description"])
    for sectorName, sector in event["sectors"].items():
        if sector["price"] is None:
            print(f"- {sectorName}: No definido")
        else:
            print(f"- {sectorName}: ${sector['price']:.2f}")

    selectedSector = None
    while selectedSector is None:
        sectorName = input_helpers.prompt_non_empty_field("\nIngrese el nombre del sector: ")
        if sectorName.lower() == "q":
            return

        for name in event["sectors"]:
            if name.lower() == sectorName.lower():
                selectedSector = name
                break

        if selectedSector is None:
            show_error("No existe un sector con ese nombre.")

    sector = event["sectors"][selectedSector]
    if sector.get("price") is None:
        show_error("El sector seleccionado no tiene precio definido.")
        return

    selectedSeats = []

    if "capacity" in sector:
        available = sector["capacity"] - sector["sold"]
        if available <= 0:
            show_error("El sector está agotado.")
            return

        print(f"\nEntradas disponibles: {available}")
        while True:
            quantity = input_helpers.prompt_positive_number("Cantidad de entradas: ")
            if quantity == "q":
                return
            if quantity <= available:
                break
            show_error(
                f"No hay suficientes entradas disponibles. Disponibles: {available}"
            )

    elif "seats" in sector:
        availableSeats = []
        for rowIndex, row in enumerate(sector["seats"]):
            for columnIndex, seat in enumerate(row):
                if seat == "free":
                    availableSeats.append([rowIndex, columnIndex])

        if len(availableSeats) == 0:
            show_error("No hay butacas disponibles en este sector.")
            return

        print("\nBUTACAS DISPONIBLES")
        for index, seat in enumerate(availableSeats, start=1):
            print(f"{index}. Fila {seat[0] + 1} - Butaca {seat[1] + 1}")

        while True:
            quantity = input_helpers.prompt_positive_number("\n¿Cuántas butacas desea comprar?: ")
            if quantity == "q":
                return
            if quantity <= len(availableSeats):
                break
            show_error(f"Solo hay {len(availableSeats)} butacas disponibles.")

        while len(selectedSeats) < quantity:
            seatOption = input_helpers.prompt_positive_number(
                f"\nSeleccione la butaca {len(selectedSeats) + 1}/{quantity}: "
            )
            if seatOption == "q":
                return
            if seatOption > len(availableSeats):
                show_error("Seleccione una butaca válida.")
                continue

            selectedSeat = availableSeats[seatOption - 1]
            if selectedSeat in selectedSeats:
                show_error("Ya seleccionó esa butaca.")
                continue

            selectedSeats.append(selectedSeat)

    else:
        show_error("El sector seleccionado tiene una configuración inválida.")
        return

    total = sector["price"] * quantity
    layout_helpers.purchase_summary(event, selectedSector, quantity, selectedSeats, total)

    while True:
        confirmation = input("\n¿Confirmar compra? (s/n): ").strip().lower()
        if confirmation == "s" or confirmation == "n":
            break
        show_error("Ingrese 's' o 'n'.")

    if confirmation == "n":
        show_info("Compra cancelada.")
        input("\nPresiona ENTER para volver al menú principal...")
        return

    newOrderData = {
        "customer_id": user["id"],
        "event_id": event["id"],
        "event_name": event["name"],
        "event_datetime": event["datetime"],
        "sector": selectedSector,
        "quantity": quantity,
        "seats": selectedSeats,
        "total": total,
        "active": True,
        "purchase_date": datetime.now().strftime("%Y-%m-%dT%H:%M"),
    }

    try:
        order = order_service.create_order(newOrderData)
        show_success(f"Compra realizada exitosamente. Orden #{order['id']}")
    except (ValueError, LookupError) as error:
        show_error(f"{error}")
    input("\nPresiona ENTER para volver al menú principal...")

def show_user_orders(user):
    orders = order_service.get_orders_by_customer(user["id"])
    layout_helpers.user_orders(orders)
    input("\nPresiona ENTER para volver al menú principal...")


def cancel_order(user):
    orders = order_service.get_orders_by_customer(user["id"])
    activeOrders = []
    for order in orders:
        if order["active"]:
            activeOrders.append(order)

    if len(activeOrders) == 0:
        show_info("No tiene órdenes activas para cancelar.")
        input("\nPresiona ENTER para volver al menú principal...")
        return

    layout_helpers.user_orders(activeOrders)

    orderId = input_helpers.prompt_positive_number("\nIngrese el ID de la orden que desea cancelar: ")
    if orderId == "q":
        return

    while True:
        confirmation = input("\n¿Confirmar cancelación? (s/n): ").strip().lower()
        if confirmation == "s" or confirmation == "n":
            break
        show_error("Ingrese 's' o 'n'.")

    if confirmation == "n":
        show_info("La orden no fue cancelada.")
        input("\nPresiona ENTER para volver al menú principal...")
        return

    try:
        order_service.cancel_order(orderId, user["id"])
        show_success(f"Orden #{orderId} cancelada exitosamente.")
    except (ValueError, LookupError, PermissionError) as error:
        show_error(f"{error}")

    input("\nPresiona ENTER para volver al menú principal...")
