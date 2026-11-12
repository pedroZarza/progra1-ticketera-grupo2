from repositories import event_repository
from services import venue_service
from datetime import datetime
from functools import reduce


# def get_all_events():
#     events = event_repository.load_events()
#     events.sort(key=lambda event: event["datetime"])
#     return events

def get_active_events():
    events = event_repository.load_events()
    activeEvents = []
    currentDate = datetime.now()

    for event in events:
        eventDate = datetime.fromisoformat(event["datetime"])
        if (
            event["status"] == "active"
            and eventDate > currentDate
        ):
            activeEvents.append(event)

    activeEvents.sort(key=lambda event: event["datetime"])
    return activeEvents


def get_events_available_for_purchase():
    events = get_active_events()
    availableEvents = []

    for event in events:
        if has_availability(event):
            availableEvents.append(event)

    return availableEvents



def has_availability(event):
    for sector in event["sectors"].values():
        if "capacity" in sector and sector["sold"] < sector["capacity"]:
            return True

        if "seats" in sector:
            for row in sector["seats"]:
                if "free" in row:
                    return True
    return False


def get_event_by_id(eventId):
    activeEvents = get_active_events()
    for event in activeEvents:
        if event["id"] == eventId:
            return event
    raise LookupError(f"No existe un evento con id '{eventId}'")


def get_events_by_organizer(organizerId):
    events = get_active_events()
    organizerEvents = []
    for event in events:
        if event["organizerId"] == organizerId:
            organizerEvents.append(event)
    return organizerEvents


def get_events_by_search(query):
    events = get_active_events()
    q = query.lower()
    matchEvents = list(
        filter(
            lambda event: q in event["name"].lower()
            or q in event["description"].lower()
            or q in event["venue"].lower()
            or q in [cat.lower() for cat in event["categories"]],
            events,
        )
    )
    return matchEvents


def get_events_by_category(categories):
    events = get_active_events()
    matchEvents = []
    for event in events:
        for category in event["categories"]:
            if category.lower() in categories:
                matchEvents.append(event)
                break
    return matchEvents


def get_available_time_slots(venueId, date):
    venue = venue_service.get_venue_by_id(venueId)
    if venue["active"] == False:
        raise ValueError("El venue seleccionado está inactivo.")

    selectedDate = datetime.strptime(date, "%d/%m/%Y").date()
    events = event_repository.load_events()
    occupiedSlots = []
    for event in events:
        existingDate = datetime.fromisoformat(event["datetime"])
        sameVenue = event["venueId"] == venue["id"]
        sameDay = existingDate.date() == selectedDate
        if sameVenue and sameDay and event["status"] != "canceled":
            occupiedSlots.append(existingDate.strftime("%H:%M"))

    availableSlots = []
    currentDate = datetime.now()
    for timeSlot in venue["time_slots"]:
        slotDate = datetime.strptime(f"{date} {timeSlot}", "%d/%m/%Y %H:%M")
        if timeSlot not in occupiedSlots and slotDate >= currentDate:
            availableSlots.append(timeSlot)

    if len(availableSlots) == 0:
        raise ValueError("No hay horarios disponibles para este venue en esa fecha.")

    return availableSlots


def create_event(organizerId, name, description, date, time, selectedCategories, venueId):
    venue = venue_service.get_venue_by_id(venueId)
    if venue["active"] == False:
        raise ValueError("El venue seleccionado está inactivo.")

    availableSlots = get_available_time_slots(venueId, date)
    if time not in availableSlots:
        raise ValueError(
            f"El horario {time} no está disponible para este venue en esa fecha. Opciones: {', '.join(availableSlots)}"
        )

    eventDate = datetime.strptime(f"{date} {time}", "%d/%m/%Y %H:%M")

    events = event_repository.load_events()

    eventSectors = {}
    for sectorName, sectorData in venue["sectors"].items():
        if sectorData["type"] == "general":
            eventSectors[sectorName] = {
                "price": None,
                "capacity": sectorData["capacity"],
                "sold": 0
            }
        elif sectorData["type"] == "numbered":
            seats = []
            for row in range(sectorData["rows"]):
                seatRow = []
                for column in range(sectorData["columns"]):
                    seatRow.append("free")
                seats.append(seatRow)
            eventSectors[sectorName] = {
                "price": None,
                "seats": seats
            }

    if len(events) > 0:
        newId = events[-1]["id"] + 1
    else:
        newId = 1

    newEvent = {
        "id": newId,
        "name": name,
        "datetime": eventDate.strftime("%Y-%m-%dT%H:%M"),
        "venue": venue["name"],
        "venueId": venue["id"],
        "categories": selectedCategories,
        "description": description,
        "organizerId": organizerId,
        "status": "active",
        "sectors": eventSectors
    }
    events.append(newEvent)
    event_repository.save_events(events)
    return newEvent


def update_sector_price(eventId, sectorName, price):
    event = get_event_by_id(eventId)
    if sectorName not in event["sectors"]:
        raise ValueError(f"El sector {sectorName} no existe.")

    events = event_repository.load_events()
    for storedEvent in events:
        if storedEvent["id"] == event["id"]:
            storedEvent["sectors"][sectorName]["price"] = price
            event_repository.save_events(events)
            return storedEvent

    raise LookupError(f"No existe un evento con id '{eventId}'")





# def get_events_by_organizer_service(organizerId):

#     organizerEvents = list(filter(
#         lambda event: str(event.get("organizerId")) == str(organizerId),
#         events
#     ))

#     organizerEvents.sort(key=lambda event: event.get("datetime", ""))

#     return organizerEvents

# def search_organizer_events_by_name_service(search_term, organizerId):

#     my_events = get_events_by_organizer_service(organizerId)

#     found_events = [
#         event for event in my_events
#         if search_term.lower() == event.get("name", "").lower()
#     ]

#     return found_events

# def search_organizer_events_by_category_service(category_term, organizerId):
#     my_events = get_events_by_organizer_service(organizerId)
#     term = category_term.lower().strip()

#     found_events = []

#     for event in my_events:
#         event_categories = list(map(
#             lambda category: str(category).lower(),
#             event.get("categories", [])
#         ))

#         match_in_list = False

#         for category in event_categories:
#             if term in category:
#                 match_in_list = True

#         if match_in_list:
#             found_events.append(event)

#     return found_events

# def update_event_service(organizerId, eventId, name=None, description=None, category=None):
#     my_events = get_events_by_organizer_service(organizerId)

#     matching_events = [
#         e for e in my_events
#         if str(e.get("id")) == str(eventId) or str(e.get("id")).startswith(str(eventId))
#     ]

#     if not matching_events:
#         raise ValueError("El evento no existe o no tenés permisos para modificarlo.")

#     if len(matching_events) > 1:
#         raise ValueError("Se encontraron múltiples eventos con ese prefijo de ID. Por favor, ingrese más caracteres para ser específico.")

#     event = matching_events[0]
#     validated_name = None
#     validated_desc = None
#     validated_cat = None

#     if name is not None and name.strip() != "":
#         if not all(char.isalnum() or char.isspace() for char in name):
#             raise ValueError("El nombre del evento no puede contener caracteres especiales.")
#         validated_name = name

#     if description is not None and description.strip() != "":
#         if not all(char.isalnum() or char.isspace() for char in description):
#             raise ValueError("La descripción no puede contener caracteres especiales.")
#         validated_desc = description

#     if category is not None and category.strip() != "":
#         matchedCategory = next((c for c in categories if c.lower() == category.lower()), None)
#         if not matchedCategory:
#             raise ValueError(f"Categoría inexistente. Opciones válidas: {', '.join(categories)}")
#         validated_cat = matchedCategory

#     if validated_name is not None:
#         event["name"] = validated_name

#     if validated_desc is not None:
#         event["description"] = validated_desc

#     if validated_cat is not None:
#         event["categories"] = [validated_cat]

#     return event

# def get_organizer_event_by_id_service(organizerId, eventId):
#     for event in events:
#         same_organizer = str(event.get("organizerId")) == str(organizerId)
#         same_event = str(event.get("id"))[:8] == str(eventId)

#         if same_organizer and same_event:
#             return event

#     return None
# def update_event_prices_service(organizerId, eventId, prices):
#     event = get_organizer_event_by_id_service(organizerId, eventId)

#     if event is None:
#         raise ValueError("El evento no existe o no pertenece al organizador.")

#     if "sectors" not in event:
#         raise ValueError("El evento no tiene sectores configurados.")

#     for sectorName, price in prices.items():

#         if sectorName not in event["sectors"]:
#             raise ValueError(f"El sector {sectorName} no existe.")

#         if price <= 0:
#             raise ValueError("El precio debe ser mayor a cero.")

#         event["sectors"][sectorName]["price"] = price

#     return event

# def get_event_sales_status_service(organizerId, eventId):

#     event = get_organizer_event_by_id_service(organizerId, eventId)

#     if event is None:
#         raise ValueError("El evento no existe o no pertenece al organizador.")

#     if "sectors" not in event:
#         raise ValueError("El evento no tiene sectores configurados.")

#     sectorStats = []

#     totalCapacity = 0
#     totalSold = 0
#     totalAvailable = 0

#     for sectorName, sectorData in event["sectors"].items():

#         if "capacity" in sectorData:
#             capacity = sectorData["capacity"]
#             sold = sectorData["sold"]
#             available = capacity - sold

#         elif "seats" in sectorData:
#             capacity = reduce(
#                 lambda total, row: total + len(row),
#                 sectorData["seats"],
#                 0
#             )

#             available = reduce(
#                 lambda total, row: total + row.count("free"),
#                 sectorData["seats"],
#                 0
#             )

#             sold = capacity - available

#         else:
#             capacity = 0
#             sold = 0
#             available = 0

#         if capacity > 0:
#             occupancy = (sold * 100) / capacity
#         else:
#             occupancy = 0

#         sectorStats.append({
#             "name": sectorName,
#             "capacity": capacity,
#             "sold": sold,
#             "available": available,
#             "occupancy": occupancy
#         })

#         totalCapacity += capacity
#         totalSold += sold
#         totalAvailable += available

#     if totalCapacity > 0:
#         totalOccupancy = (totalSold * 100) / totalCapacity
#     else:
#         totalOccupancy = 0

#     return {
#         "event": event,
#         "sectors": sectorStats,
#         "totalCapacity": totalCapacity,
#         "totalSold": totalSold,
#         "totalAvailable": totalAvailable,
#         "totalOccupancy": totalOccupancy
#     }
# def assign_category_service(organizerId, eventId, category):

#     my_events = get_events_by_organizer_service(organizerId)

#     matching_events = [
#         e for e in my_events
#         if str(e.get("id")) == str(eventId) or str(e.get("id")).startswith(str(eventId))
#     ]

#     if not matching_events:
#         raise ValueError("El evento no existe o no tenés permisos para modificarlo.")

#     if len(matching_events) > 1:
#         raise ValueError("Se encontraron múltiples eventos con ese prefijo de ID. Por favor, ingrese más caracteres para ser específico.")

#     event = matching_events[0]

#     if not category:
#         raise ValueError("Debe ingresar una categoría válida.")

#     matchedCategory = next((c for c in categories if c.lower() == category.lower()), None)
#     if not matchedCategory:
#         raise ValueError(f"Categoría inexistente. Opciones válidas: {', '.join(categories)}")

#     event["categories"] = [matchedCategory]

#     return event

# def update_event_availability_service(event_id, sector_name, quantity, selected_seats):
#     event = get_event_by_id(str(event_id))

#     if event is None:
#         return False

#     if sector_name not in event["sectors"]:
#         return False

#     sector = event["sectors"][sector_name]

#     if "capacity" in sector:
#         available = sector["capacity"] - sector["sold"]

#         if quantity > available:
#             return False

#         sector["sold"] += quantity

#     elif "seats" in sector:
#         for seat in selected_seats:
#             row = seat[0]
#             column = seat[1]

#             if sector["seats"][row][column] != "free":
#                 return False

#         for seat in selected_seats:
#             row = seat[0]
#             column = seat[1]

#             sector["seats"][row][column] = "occupied"

#     return True

# def search_active_events_by_name_service(search_term):
#     active_events = get_active_events()
#     found_events = []

#     term = search_term.lower().strip()

#     for event in active_events:
#         if term in event["name"].lower():
#             found_events.append(event)

#     return found_events


