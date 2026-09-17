from utils import input_helpers, layout_helpers
from services import event_service, order_service
from utils.messages import show_error, show_success, show_info, show_warning
from datetime import datetime

def buy_tickets(user):
    events = event_service.read_active_events()
    if len(events) == 0:
        show_info("No hay eventos disponibles.")
        return
    
    layout_helpers.events_board(events)
    
    event_id = input_helpers.prompt_non_empty_field("\nIngrese el ID del evento: ")
    if event_id.lower() == "q": return

    event = event_service.get_event_by_id(event_id)

    if event is None:
        show_error("No existe un evento con ese ID.")
        return

    eventDatetime = datetime.fromisoformat(event["datetime"])
    formattedDatetime = eventDatetime.strftime("%d/%m/%Y %H:%M")

    print(f"\nSELECCIÓN DE SECTOR | {event['name']} - {formattedDatetime}")
    print(event["description"])

    for sector_name, sector in event["sectors"].items():
        print(f"- {sector_name}: ${sector['price']}")
        
    selected_sector = None
    while selected_sector is None:
        sector_name = input_helpers.prompt_non_empty_field(
            "\nIngrese el nombre del sector: "
        )
        if sector_name.lower() == "q":
            return
        
        for name, sector in event["sectors"].items():
            if name.lower() == sector_name.lower():
                selected_sector = name
                break
        if selected_sector is None:
            show_error("No existe un sector con ese nombre.")
    
    
    sector = event["sectors"][selected_sector]
    selected_seats = []
    if "capacity" in sector:
        available = sector["capacity"] - sector["sold"]

        print(f"\nEntradas disponibles: {available}")

        while True:
            quantity = input_helpers.prompt_positive_number(
                "Cantidad de entradas: "
            )

            if quantity <= available:
                break

            show_error(
                f"No hay suficientes entradas disponibles. "
                f"Disponibles: {available}"
            )
            
        
    else:
        available_seats = []
        for i in range(len(sector["seats"])):
            for j in range(len(sector["seats"][i])):
                if sector["seats"][i][j] == "free":
                    available_seats.append([i, j])

        print("\nBUTACAS DISPONIBLES")

        for i in range(len(available_seats)):
            row = available_seats[i][0]
            column = available_seats[i][1]

            print(f"{i + 1}. Fila {row + 1} - Butaca {column + 1}")

        while True:
            quantity = input_helpers.prompt_positive_number("\n¿Cuántas butacas desea comprar?: ")
            if quantity <= len(available_seats):
                break

            show_error(f"Solo hay {len(available_seats)} butacas disponibles.")

        for i in range(quantity):
            while True:
                seat_option = input_helpers.prompt_positive_number(f"\nSeleccione la butaca {i + 1}/{quantity}: ")

                if seat_option > len(available_seats):
                    show_error("Seleccione una butaca válida.")
                    continue

                selected_seat = available_seats[seat_option - 1]

                if selected_seat in selected_seats:
                    show_error("Ya seleccionó esa butaca.")
                    continue

                selected_seats.append(selected_seat)
                break
        
    total = sector["price"] * quantity
    print("\n=====RESUMEN DE COMPRA=====")
    print(f"Evento: {event['name']}")
    print(f"Sector: {selected_sector}")
    print(f"Cantidad de entradas: {quantity}")

    if len(selected_seats) > 0:
        print("Butacas seleccionadas:")

        for seat in selected_seats:
            print(f"- Fila {seat[0] + 1} - Butaca {seat[1] + 1}")

    print(f"Total: ${total}")
    
    while True:
        confirmation = input("\n¿Confirmar compra? (s/n): ").lower()

        if confirmation == "s" or confirmation == "n":
            break

        show_error("Ingrese 's' o 'n'.")

    if confirmation == "n":
        show_info("Compra cancelada.")
        return   
        
    newOrderData = {
        "customer_id": user["id"],
        "event_id": event["id"],
        "sector": selected_sector,
        "quantity": quantity,
        "seats": selected_seats,
        "total": total,
        "status": "active",
    }   
    success, order = order_service.create_order(newOrderData)
    if success:
        ##aca va función del service de evento que actualice su capacidad
        show_success(f"Compra realizada exitosamente. Orden #{order['id']}")

            
def show_user_orders(user):
    orders = order_service.get_orders_by_customer(user["id"])

    if len(orders) == 0:
        show_info("No tiene tickets comprados.")
        return

    print("\n=====MIS TICKETS=====")

    for order in orders:
        print(f"\nOrden #{order['id']}")
        print(f"Evento: {order['event_id']}")
        print(f"Sector: {order['sector']}")
        print(f"Cantidad de tickets: {order['quantity']}")

        if len(order["seats"]) > 0:
            print("Butacas:")

            for seat in order["seats"]:
                print(f"- Fila {seat[0]} - Butaca {seat[1]}")

        print(f"Total: ${order['total']}")
        print(f"Estado: {order['status']}")
        print("----------------------------------------------------------")
        
    input("\nPresiona ENTER para volver al menú principal...")
    return