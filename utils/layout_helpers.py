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
        print(f"\n[{event['id']}] {event['name']}")
        print(f"    📅 {date} | 🕒 {time} | 📍 {event['venue']} | 🎭 {", ".join(event["categories"])}\n")


def event_detail(event):
    datetime_obj = datetime.fromisoformat(event["datetime"])
    date = datetime_obj.strftime("%d-%m-%Y")
    time = datetime_obj.strftime("%H:%M")

    print("\n==========================================================")
    print("                    DETALLE DEL EVENTO")
    print("==========================================================")
    print(f"Evento: {event['name']}")
    print(f"Fecha: {date}")
    print(f"Hora: {time}")
    print(f"Lugar: {event['venue']}")
    print(f"Categorías: {', '.join(event['categories'])}")
    print(f"Descripción: {event['description']}")
    print("----------------------------------------------------------")
    print("Sectores y disponibilidad:")

    if len(event["sectors"]) == 0:
        show_info("El evento todavía no tiene sectores configurados.")
        return

    total_event_capacity = 0
    total_event_available = 0

    for sector_name, sector_data in event["sectors"].items():
        price = sector_data["price"]

        if "capacity" in sector_data:
            capacity = sector_data["capacity"]
            sold = sector_data["sold"]
            available = capacity - sold

        elif "seats" in sector_data:
            seats = sector_data["seats"]
            capacity = 0
            available = 0

            for row in seats:
                for seat in row:
                    capacity += 1

                    if seat == "free":
                        available += 1

            sold = capacity - available

        total_event_capacity += capacity
        total_event_available += available

        if capacity > 0:
            occupancy = (sold * 100) / capacity
        else:   
            occupancy = 0

        print(f"\nSector: {sector_name}")
        print(f"Precio: ${price}")
        print(f"Capacidad total: {capacity}")
        print(f"Disponibles: {available}")
        print(f"Ocupados: {sold}")
        print(f"Ocupación: {occupancy:.1f}%")

    total_event_sold = total_event_capacity - total_event_available

    if total_event_capacity > 0:
        total_occupancy = (total_event_sold * 100) / total_event_capacity
    else:
        total_occupancy = 0

    print("\n----------------------------------------------------------")
    print("RESUMEN GENERAL DEL EVENTO")
    print(f"Capacidad total: {total_event_capacity}")
    print(f"Lugares disponibles: {total_event_available}")
    print(f"Lugares ocupados: {total_event_sold}")
    print(f"Ocupación total: {total_occupancy:.1f}%")
    