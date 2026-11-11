from datetime import datetime
from utils.messages import show_info, show_error, show_success, show_warning


# def events_board(events):
#     print("\n==========================================================")
#     print("                    CARTELERA - EVENTPASS")
#     print("==========================================================")
#     if len(events) == 0:
#         show_info("No hay eventos disponibles en este momento.")
#         return    
#     for event in events:
#         datetimeObj = datetime.fromisoformat(event["datetime"])
#         date = datetimeObj.strftime("%d-%m-%Y")
#         time = datetimeObj.strftime("%H:%M")
        
#         print(f"\n[{str(event['id'])[:8]}] {event['name']}") 
#         print(f"    📅 {date} | 🕒 {time} | 📍 {event['venue']} | 🎭 {', '.join(event['categories'])}\n")


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
    print("-" * 45)
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

        print(f"- {sectorName}: ${sector['price']} | Disponibles: {available}{warning}")

    print("-" * 45)
        
        
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