from datetime import datetime
from utils.messages import show_info



def events_board(events):
    """Imprime la cartelera de eventos con su disponibilidad.

    Parámetros:
        events (list): eventos a mostrar.
    """
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
    """Imprime el detalle de un evento y sus sectores.

    Parámetros:
        event (dict): evento a consultar.
        organizer (dict o None): organizador del evento.
    """
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
    """Imprime el listado de venues.

    Parámetros:
        venues (list): venues a mostrar.
    """
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
    """Imprime el detalle de un venue y su capacidad.

    Parámetros:
        venue (dict): venue a mostrar.
    """
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
    """Imprime el resumen de una compra antes de confirmarla.

    Parámetros:
        event (dict): evento a consultar.
        sectorName (str): sector elegido.
        quantity (int): cantidad de entradas.
        selectedSeats (list): butacas elegidas, cada una como [fila, columna].
        total (float): importe total.
    """
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
    """Imprime las órdenes de un usuario.

    Parámetros:
        orders (list): órdenes a mostrar.
    """
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
    """Imprime los eventos de un organizador con su estado.

    Parámetros:
        events (list): eventos a mostrar.
    """
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
    """Imprime las órdenes activas de un evento.

    Parámetros:
        event (dict): evento a consultar.
        orders (list): órdenes a mostrar.
    """
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



def count_sold_seats(row, index=0):
    """Cuenta de forma recursiva las butacas ocupadas de una fila.

    Parámetros:
        row (list): estados de las butacas.
        index (int): posición desde la que cuenta. Por defecto 0.

    Retorna:
        int: cantidad de butacas ocupadas.
    """
    if index == len(row):
        return 0
    if row[index] == "occupied":
        return 1 + count_sold_seats(row, index + 1)
    return count_sold_seats(row, index + 1)


def build_event_sales_summary(event):
    """Calcula vendidas, disponibles, recaudación y estado del evento.

    Parámetros:
        event (dict): evento a consultar.

    Retorna:
        dict: totales, ocupación, estado y detalle por sector.
    """
    eventDatetime = datetime.fromisoformat(event["datetime"])

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
                capacity += len(row)
                sold += count_sold_seats(row)

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

    return {
        "datetime": eventDatetime,
        "status": status,
        "total_sold": totalSold,
        "total_capacity": totalCapacity,
        "available": availableTotal,
        "revenue": totalRevenue,
        "occupancy": occupancyPercentage,
        "sectors": sectors,
    }


def event_status_summary(event):
    """Imprime el resumen de ventas y ocupación de un evento.

    Parámetros:
        event (dict): evento a consultar.
    """
    summary = build_event_sales_summary(event)
    formattedDatetime = summary["datetime"].strftime("%d/%m/%Y %H:%M")

    print(f"\n[{event['id']}] {event['name']}")
    print(f"{formattedDatetime}  |  {event['venue']}")
    print(f"Estado: {summary['status']}")
    print(f"\nVendidas:      {summary['total_sold']} / {summary['total_capacity']}  ({summary['occupancy']:.0f}%)")
    print(f"Disponibles:   {summary['available']}")
    print(f"Recaudado:     ${summary['revenue']:.2f}")
    print("\nSectores:")
    for sector in summary["sectors"]:
        print(
            f"{sector['name']}: {sector['sold']} vendidas, "
            f"{sector['available']} libres, ${sector['revenue']:.2f}"
        )
    print()
