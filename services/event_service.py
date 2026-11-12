from repositories import event_repository
from services import venue_service, order_service
from datetime import datetime
from functools import reduce


def get_active_events():
    """Devuelve los eventos activos y futuros, ordenados por fecha.

    Retorna:
        list: eventos activos todavía no realizados.
    """
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


def has_availability(event):
    """Indica si algún sector del evento tiene lugares libres.

    Parámetros:
        event (dict): evento a consultar.

    Retorna:
        bool: True si queda disponibilidad.
    """
    for sector in event["sectors"].values():
        if "capacity" in sector and sector["sold"] < sector["capacity"]:
            return True

        if "seats" in sector:
            for row in sector["seats"]:
                if "free" in row:
                    return True
    return False


def get_event_by_id(eventId):
    """Busca un evento activo por ID.

    Parámetros:
        eventId (int): identificador del evento.

    Retorna:
        dict: el evento activo.
    """
    activeEvents = get_active_events()
    for event in activeEvents:
        if event["id"] == eventId:
            return event
    raise LookupError(f"No existe un evento con id '{eventId}'")


def get_any_event_by_id(eventId):
    """Busca un evento por ID, sin filtrar por estado.

    Parámetros:
        eventId (int): identificador del evento.

    Retorna:
        dict: el evento encontrado.
    """
    events = event_repository.load_events()
    for event in events:
        if event["id"] == eventId:
            return event
    raise LookupError(f"No existe un evento con id '{eventId}'")

def get_events_by_search(query):
    """Filtra eventos activos por nombre, descripción, venue o categoría.

    Parámetros:
        query (str): texto a buscar.

    Retorna:
        list: eventos que coinciden.
    """
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
    """Filtra eventos activos que coinciden con alguna categoría.

    Parámetros:
        categories (list): nombres de categoría en minúsculas.

    Retorna:
        list: eventos que coinciden.
    """
    events = get_active_events()
    matchEvents = []
    for event in events:
        for category in event["categories"]:
            if category.lower() in categories:
                matchEvents.append(event)
                break
    return matchEvents


def get_events_by_organizer(organizerId):
    """Devuelve los eventos activos de un organizador.

    Parámetros:
        organizerId (int): identificador del organizador.

    Retorna:
        list: eventos activos del organizador.
    """
    events = get_active_events()
    organizerEvents = []
    for event in events:
        if event["organizerId"] == organizerId:
            organizerEvents.append(event)
    return organizerEvents


def get_event_by_organizer(organizerId, eventId):
    """Busca un evento activo que pertenezca al organizador.

    Parámetros:
        organizerId (int): identificador del organizador.
        eventId (int): identificador del evento.

    Retorna:
        dict: el evento activo del organizador.
    """
    events = get_events_by_organizer(organizerId)
    for event in events:
        if event["id"] == eventId:
            return event
    raise LookupError(f"No posee un evento registrado con id '{eventId}'")


def get_all_events_by_organizer(organizerId):
    """Devuelve todos los eventos de un organizador.

    Parámetros:
        organizerId (int): identificador del organizador.

    Retorna:
        list: eventos del organizador, ordenados por fecha.
    """
    events = event_repository.load_events()
    organizerEvents = []
    for event in events:
        if event["organizerId"] == organizerId:
            organizerEvents.append(event)
    organizerEvents.sort(key=lambda event: event["datetime"])
    return organizerEvents

def get_any_event_by_organizer(organizerId, eventId):
    """Busca cualquier evento del organizador por ID.

    Parámetros:
        organizerId (int): identificador del organizador.
        eventId (int): identificador del evento.

    Retorna:
        dict: el evento del organizador.
    """
    events = get_all_events_by_organizer(organizerId)
    for event in events:
        if event["id"] == eventId:
            return event
    raise LookupError(f"No posee un evento registrado con id '{eventId}'")


def get_events_history(organizerId):
    """Devuelve los eventos cancelados o ya ocurridos del organizador.

    Parámetros:
        organizerId (int): identificador del organizador.

    Retorna:
        list: historial ordenado del más reciente al más antiguo.
    """
    events = event_repository.load_events()
    history = []
    currentDate = datetime.now()

    for event in events:
        eventDate = datetime.fromisoformat(event["datetime"])
        if event["organizerId"] == organizerId and (
            event["status"] == "cancelled" or eventDate <= currentDate):
            history.append(event)

    history.sort(key=lambda event: event["datetime"], reverse=True)
    return history



def get_available_time_slots(venueId, date):
    """Lista los horarios libres de un venue en una fecha.

    Parámetros:
        venueId (int): identificador del venue.
        date (str): fecha en formato DD/MM/AAAA.

    Retorna:
        list: horarios disponibles, en formato HH:MM.
    """
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
        if sameVenue and sameDay and event["status"] != "cancelled":
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
    """Crea un evento activo y copia los sectores del venue.

    Parámetros:
        organizerId (int): identificador del organizador.
        name (str): nombre del evento.
        description (str): descripción del evento.
        date (str): fecha en formato DD/MM/AAAA.
        time (str): horario en formato HH:MM.
        selectedCategories (list): categorías del evento.
        venueId (int): identificador del venue.

    Retorna:
        dict: el evento creado.
    """
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


def restore_event_availability(eventId, sectorName, quantity, seats):
    """Devuelve entradas o butacas al cancelar una compra.

    Parámetros:
        eventId (int): identificador del evento.
        sectorName (str): sector de la orden.
        quantity (int): cantidad de entradas a devolver.
        seats (list): butacas a liberar, cada una como [fila, columna].

    Retorna:
        dict: el evento actualizado.
    """
    event = get_event_by_id(eventId)
    events = event_repository.load_events()
    for storedEvent in events:
        if storedEvent["id"] == event["id"]:
            storedSector = storedEvent["sectors"][sectorName]
            if "capacity" in storedSector:
                storedSector["sold"] -= quantity
            else:
                for seat in seats:
                    storedSector["seats"][seat[0]][seat[1]] = "free"
            event_repository.save_events(events)
            return storedEvent

    raise LookupError(f"No existe un evento con id '{eventId}'")


def update_sector_price(eventId, sectorName, price):
    """Actualiza el precio de un sector del evento.

    Parámetros:
        eventId (int): identificador del evento.
        sectorName (str): nombre del sector.
        price (float): nuevo precio.

    Retorna:
        dict: el evento actualizado.
    """
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
    """Agrega una categoría al evento si todavía no la tiene.

    Parámetros:
        eventId (int): identificador del evento.
        category (str): categoría a asignar.

    Retorna:
        dict: el evento actualizado.
    """
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
    """Quita una categoría del evento, dejando al menos una.

    Parámetros:
        eventId (int): identificador del evento.
        category (str): categoría a quitar.

    Retorna:
        dict: el evento actualizado.
    """
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
    """Actualiza nombre y descripción si el evento es del organizador.

    Parámetros:
        eventId (int): identificador del evento.
        organizerId (int): identificador del organizador.
        name (str): nuevo nombre.
        description (str): nueva descripción.

    Retorna:
        dict: el evento actualizado.
    """
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
    """Cancela el evento si es del organizador y no tiene órdenes activas.

    Parámetros:
        eventId (int): identificador del evento.
        organizerId (int): identificador del organizador.

    Retorna:
        dict: el evento cancelado.
    """
    event = get_event_by_id(eventId)
    orders = order_service.get_active_orders_by_event_id(eventId)
    if len(orders) > 0:
        raise ValueError("El evento posee órdenes activas y no puede ser cancelado.")
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

def get_event_orders(eventId):
    """Devuelve las órdenes activas de un evento.

    Parámetros:
        eventId (int): identificador del evento.

    Retorna:
        list: órdenes activas del evento.
    """
    orders = order_service.get_active_orders_by_event_id(eventId)
    if len(orders) == 0:
        raise LookupError(f"El evento con id '{eventId}' no posee órdenes activas.")
    return orders
