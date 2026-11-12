from repositories import event_repository
from services import venue_service
from datetime import datetime
from functools import reduce


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


def get_events_by_organizer(organizerId):
    events = get_active_events()
    organizerEvents = []
    for event in events:
        if event["organizerId"] == organizerId:
            organizerEvents.append(event)
    return organizerEvents


def get_event_by_organizer(organizerId, eventId):
    events = get_events_by_organizer(organizerId)
    for event in events:
        if event["id"] == eventId:
            return event
    raise LookupError(f"No posee un evento registrado con id '{eventId}'")


def get_events_history(organizerId):
    events = event_repository.load_events()
    history = []
    currentDate = datetime.now()

    for event in events:
        eventDate = datetime.fromisoformat(event["datetime"])
        if event["organizerId"] == organizerId and (
            event["status"] == "canceled" or eventDate <= currentDate
        ):
            history.append(event)

    history.sort(key=lambda event: event["datetime"], reverse=True)
    return history



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


def add_event_category(eventId, category):
    event = get_event_by_id(eventId)
    for existingCategory in event["categories"]:
        if existingCategory.lower() == category.lower():
            raise ValueError("El evento ya tiene esa categoría.")
    events = event_repository.load_events()
    for storedEvent in events:
        if storedEvent["id"] == event["id"]:
            storedEvent["categories"].append(category)
            event_repository.save_events(events)
            return storedEvent
    raise LookupError(f"No existe un evento con id '{eventId}'")


def remove_event_category(eventId, category):
    event = get_event_by_id(eventId)
    if len(event["categories"]) == 1:
        raise ValueError("El evento debe conservar al menos una categoría.")

    matchedCategory = None
    for existingCategory in event["categories"]:
        if existingCategory.lower() == category.lower():
            matchedCategory = existingCategory
            break
    if matchedCategory is None:
        raise ValueError("El evento no tiene esa categoría.")

    events = event_repository.load_events()
    for storedEvent in events:
        if storedEvent["id"] == event["id"]:
            storedEvent["categories"].remove(matchedCategory)
            event_repository.save_events(events)
            return storedEvent
    raise LookupError(f"No existe un evento con id '{eventId}'")


def update_event_info(eventId, organizerId, name, description):
    event = get_event_by_id(eventId)
    if event["organizerId"] != organizerId:
        raise PermissionError("El evento no pertenece al organizador.")

    events = event_repository.load_events()
    for storedEvent in events:
        if storedEvent["id"] == event["id"]:
            storedEvent["name"] = name
            storedEvent["description"] = description
            event_repository.save_events(events)
            return storedEvent
    raise LookupError(f"No existe un evento con id '{eventId}'")


def cancel_event(eventId, organizerId):
    event = get_event_by_id(eventId)
    if event["organizerId"] != organizerId:
        raise PermissionError("El evento no pertenece al organizador.")
    if event["status"] == "cancelled":
        raise ValueError("El evento ya se encuentra cancelado.")

    events = event_repository.load_events()
    for storedEvent in events:
        if storedEvent["id"] == event["id"]:
            storedEvent["status"] = "cancelled"
            event_repository.save_events(events)
            return storedEvent
    raise LookupError(f"No existe un evento con id '{eventId}'")


def get_event_sales(event):
    sectors = []
    totalSold = 0
    totalCapacity = 0
    totalRevenue = 0

    for sectorName, sector in event["sectors"].items():
        if "capacity" in sector:
            capacity = sector["capacity"]
            sold = sector["sold"]
        elif "seats" in sector:
            capacity = 0
            sold = 0
            for row in sector["seats"]:
                for seat in row:
                    capacity += 1
                    if seat == "occupied":
                        sold += 1
        else:
            capacity = 0
            sold = 0

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
            "capacity": capacity,
            "revenue": revenue
        })

    return {
        "sectors": sectors,
        "totalSold": totalSold,
        "totalAvailable": totalCapacity - totalSold,
        "totalRevenue": totalRevenue
    }



