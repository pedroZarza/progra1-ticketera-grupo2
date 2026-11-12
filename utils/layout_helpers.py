from datetime import datetime
from utils.messages import show_info, show_error, show_success, show_warning



def events_board(events):
    print("\n==========================================================")
    print("                    CARTELERA - EVENTPASS")
    print("==========================================================")

    if len(events) == 0:
        show_info("No hay eventos disponibles en este momento.")
        return

    for event in events:
        datetimeObj = datetime.fromisoformat(event["datetime"])
        date = datetimeObj.strftime("%d-%m-%Y")
        time = datetimeObj.strftime("%H:%M")

        totalCapacity = 0
        totalAvailable = 0

        for sector in event["sectors"].values():

            if "capacity" in sector:
                capacity = sector["capacity"]
                available = capacity - sector["sold"]

            elif "seats" in sector:
                capacity = 0
                available = 0

                for row in sector["seats"]:
                    for seat in row:
                        capacity += 1

                        if seat == "free":
                            available += 1
            else:
                capacity = 0
                available = 0

            totalCapacity += capacity
            totalAvailable += available
            
        warning = ""
        if totalCapacity > 0:
            if totalAvailable == 0:
                warning = " | SOLD OUT"
            elif totalAvailable <= totalCapacity * 0.15:
                warning = " | ¡ÚLTIMAS ENTRADAS!"

        print(f"\n[{str(event['id'])[:8]}] {event['name']}{warning}")
        print(f"    📅 {date} | 🕒 {time} | 📍 {event['venue']} | 🎭 {', '.join(event['categories'])}\n")


def event_detail(event, organizer):
    eventDatetime = datetime.fromisoformat(event["datetime"])
    formattedDatetime = eventDatetime.strftime("%d/%m/%Y %H:%M")

    print(f"\n[{event['id']}] {event['name']}")
    print("-" * 58)
    print(f"Fecha y hora: {formattedDatetime}")
    print(f"Lugar: {event['venue']}")
    print(f"Categorías: {', '.join(event['categories'])}")

    if organizer is not None:
        print(f"Organizador: {organizer['username']}")
    else:
        print("Organizador: No disponible")

    print(f"\nDescripción: {event['description']}")

    print("\nSectores y entradas disponibles:")

    if len(event["sectors"]) == 0:
        show_info("El evento todavía no tiene sectores configurados.")
        return

    for sectorName, sector in event["sectors"].items():

        if "capacity" in sector:
            capacity = sector["capacity"]
            available = capacity - sector["sold"]

        elif "seats" in sector:
            capacity = 0
            available = 0

            for row in sector["seats"]:
                for seat in row:
                    capacity += 1
                    if seat == "free":
                        available += 1
        else:
            capacity = 0
            available = 0
        warning = ""
        if capacity > 0:
            if available == 0:
                warning = " | SOLD OUT"
            elif available <= capacity * 0.15:
                warning = " | ¡ÚLTIMAS ENTRADAS!"

        if sector["price"] is None:
            formattedPrice = "No definido"
        else:
            formattedPrice = f"${sector['price']:.2f}"

        print(f"- {sectorName}: {formattedPrice} | Disponibles: {available}{warning}")

    print("-" * 58)
        
        
def venues_board(venues):
    print("\nVENUES DEL SISTEMA")

    for venue in venues:
        print(f"\nID: {venue['id']}")
        print(f"Nombre: {venue['name']}")
        print(f"Dirección: {venue['address']}")
        print(f"Estado: {'Activo' if venue['active'] else 'Inactivo'}")
        print("Sectores:")

        for sector_name in venue["sectors"]:
            print(f"-{sector_name}")
            
def venue_detail(venue):
    totalCapacity = 0
    for sector in venue["sectors"].values():
        if sector["type"] == "general":
            totalCapacity += sector["capacity"]
        elif sector["type"] == "numbered":
            totalCapacity += sector["rows"] * sector["columns"]
    
    print(f"\n[{venue['id']}] {venue['name']}")
    print("-" * 45)
    print(f"Dirección: {venue['address']}")
    print(f"Estado: {'Activo' if venue['active'] else 'Inactivo'}")
    print(f"Capacidad total: {totalCapacity}")
    
    print("\nSectores:")
    for sectorName, sector in venue["sectors"].items():

        if sector["type"] == "general":
            capacity = sector["capacity"]

        elif sector["type"] == "numbered":
            capacity = sector["rows"] * sector["columns"]

        print(f"-{sectorName} (Capacidad: {capacity})")
    print("-" * 45)


def purchase_summary(event, sectorName, quantity, selectedSeats, total):
    print("\n==========================================================")
    print("               RESUMEN DE COMPRA - EVENTPASS")
    print("==========================================================")
    print(f"\nEvento: {event['name']}")
    print(f"Sector: {sectorName}")
    print(f"Cantidad de entradas: {quantity}")

    if len(selectedSeats) > 0:
        print("Butacas seleccionadas:")
        for seat in selectedSeats:
            print(f"- Fila {seat[0] + 1} - Butaca {seat[1] + 1}")

    print(f"Total: ${total:.2f}")
    print("\n" + "=" * 58)


def user_orders(orders):
    print("\n==========================================================")
    print("                  MIS TICKETS - EVENTPASS")
    print("==========================================================")

    if len(orders) == 0:
        show_info("No tiene tickets comprados.")
        return

    for order in orders:
        purchaseDate = datetime.fromisoformat(order["purchase_date"])
        formattedPurchaseDate = purchaseDate.strftime("%d/%m/%Y %H:%M")

        print(f"\nOrden #{order['id']}")
        print(f"Evento: {order['event_name']}")
        print(f"Sector: {order['sector']}")
        print(f"Cantidad de tickets: {order['quantity']}")
        print(f"Fecha de compra: {formattedPurchaseDate}")

        if len(order["seats"]) > 0:
            print("Butacas:")
            for seat in order["seats"]:
                print(f"- Fila {seat[0] + 1} - Butaca {seat[1] + 1}")

        print(f"Total: ${order['total']:.2f}")
        print(f"Estado: {'Activo' if order['active'] else 'CANCELADA'}")
        print("-" * 58)



def organizer_events_board(events):
    print("\n==========================================================")
    print("                  MIS EVENTOS - EVENTPASS")
    print("==========================================================")

    if len(events) == 0:
        show_info("No tenés eventos registrados.")
        return

    for event in events:
        datetimeObj = datetime.fromisoformat(event["datetime"])
        if event["status"] == "cancelled":
            status = "CANCELADO"
        elif datetimeObj < datetime.now():
            status = "FINALIZADO"
        else:
            status = "Active"
        date = datetimeObj.strftime("%d-%m-%Y")
        time = datetimeObj.strftime("%H:%M")

        print(f"\n[{str(event['id'])[:8]}] {event['name']}")
        print(f"    Fecha: {date} | Hora: {time}")
        print(f"    Venue: {event['venue']} | Estado: {status}")

    print("\n" + "=" * 58)

def event_orders(event, orders):
    eventDatetime = datetime.fromisoformat(event["datetime"])
    formattedDatetime = eventDatetime.strftime("%d/%m/%Y %H:%M")

    print("\n----------------------------------------------------------")
    print("                    ÓRDENES ACTIVAS")
    print("----------------------------------------------------------")
    print(f"\n[{event['id']}] {event['name']}")
    print(f"Fecha y hora: {formattedDatetime}")
    print(f"Lugar: {event['venue']}")

    if len(orders) == 0:
        show_info("El evento no tiene órdenes.")
        return

    for order in orders:
        purchaseDate = datetime.fromisoformat(order["purchase_date"])
        formattedPurchaseDate = purchaseDate.strftime("%d/%m/%Y %H:%M")

        print(f"\n\nOrden #{order['id']}")
        print(f"Sector: {order['sector']}")
        print(f"Cantidad de tickets: {order['quantity']}")
        print(f"Fecha de compra: {formattedPurchaseDate}")

        if len(order["seats"]) > 0:
            print("Butacas:")
            for seat in order["seats"]:
                print(f"- Fila {seat[0] + 1} - Butaca {seat[1] + 1}")
        print("----------------------")
        print(f"Total: ${order['total']:.2f}")
        print(f"Estado: {'Activo' if order['active'] else 'CANCELADA'}")
       


def event_status_summary(event):
    eventDatetime = datetime.fromisoformat(event["datetime"])
    formattedDatetime = eventDatetime.strftime("%d/%m/%Y %H:%M")

    totalSold = 0
    totalCapacity = 0
    totalRevenue = 0
    sectors = []

    for sectorName, sector in event["sectors"].items():
        if "capacity" in sector:
            capacity = sector["capacity"]
            sold = sector["sold"]
        else:
            capacity = 0
            sold = 0
            for row in sector["seats"]:
                for seat in row:
                    capacity += 1
                    if seat == "occupied":
                        sold += 1

        available = capacity - sold
        price = sector["price"] if sector["price"] is not None else 0
        revenue = sold * price

        totalSold += sold
        totalCapacity += capacity
        totalRevenue += revenue
        sectors.append({
            "name": sectorName,
            "sold": sold,
            "available": available,
            "revenue": revenue,
        })

    availableTotal = totalCapacity - totalSold
    if totalCapacity == 0:
        occupancyPercentage = 0
    else:
        occupancyPercentage = totalSold * 100 / totalCapacity


   
    if event["status"] == "cancelled":
        status = "CANCELADO"
    elif eventDatetime < datetime.now():
        status = "FINALIZADO"
    elif totalCapacity > 0 and availableTotal == 0:
        status = "AGOTADO"
    elif totalCapacity > 0 and availableTotal <= totalCapacity * 0.15:
        status = "ÚLTIMAS ENTRADAS"
    else:
        status = "CON DISPONIBILIDAD"

    print(f"\n[{event['id']}] {event['name']}")
    print(f"{formattedDatetime}  |  {event['venue']}")
    print(f"Estado: {status}")
    print(f"\nVendidas:      {totalSold} / {totalCapacity}  ({occupancyPercentage:.0f}%)")
    print(f"Disponibles:   {availableTotal}")
    print(f"Recaudado:     ${totalRevenue:.2f}")
    print("\nSectores:")
    for sector in sectors:
        print(
            f"{sector['name']}: {sector['sold']} vendidas, "
            f"{sector['available']} libres, ${sector['revenue']:.2f}"
        )
    print()