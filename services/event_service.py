import uuid
from datetime import datetime
from data.events_data import events
from data.venues_data import venues 
from data.categories_data import categories 

def read_all_events():
    events.sort(key=lambda event: event["datetime"])
    return events

def create_event_service(organizerId, name, datetimeStr, category, venueIdStr, description):
    """
    Registra un nuevo evento validando las reglas de negocio.
    """
    # Validar que el nombre no contenga caracteres especiales
    if not all(char.isalnum() or char.isspace() for char in name):
        raise ValueError("El nombre del evento no puede contener caracteres especiales. Solo se permiten letras, números y espacios.")

    # Validar que el venue exista
    venue = next((v for v in venues if str(v["id"]) == str(venueIdStr)), None)
    if not venue:
        raise ValueError("El venue seleccionado no existe.")

    # Validar formato de la fecha y que sea una fecha futura
    try:
        eventDate = datetime.strptime(datetimeStr, "%d/%m/%Y %H:%M")
        if eventDate < datetime.now():
            raise ValueError("La fecha del evento no puede ser en el pasado.")
    except ValueError as e:
        if "does not match format" in str(e):
            raise ValueError("Formato de fecha inválido. Utilice DD/MM/AAAA HH:MM.")
        raise e

    # Validar que el horario esté dentro de los permitidos por el Venue
    eventTimeStr = eventDate.strftime("%H:%M")
    if eventTimeStr not in venue.get("time_slots", []):
        raise ValueError(f"El horario {eventTimeStr} no está disponible para este venue. Opciones: {', '.join(venue['time_slots'])}")

    # Validar disponibilidad de horario
    for event in events:
        if str(event.get("venueId")) == str(venue["id"]) and event.get("datetime") == datetimeStr and event.get("state") != "canceled":
            raise ValueError("El venue ya tiene un evento programado para esa misma fecha y horario.")

    # Validar categoría sin importar mayúsculas/minúsculas
    matchedCategory = next((c for c in categories if c.lower() == category.lower()), None)
    if not matchedCategory:
        raise ValueError(f"Categoría inexistente. Opciones válidas: {', '.join(categories)}")

    newEvent = {
        "id": str(uuid.uuid4()), 
        "organizerId": organizerId,
        "name": name,
        "datetime": datetimeStr,
        "category": matchedCategory, 
        "venueId": venue["id"], 
        "description": description,
        "state": "active",
        "sectorPrices": {sectorName: None for sectorName in venue.get("sectors", {}).keys()}
    }

    
    events.append(newEvent)
    
    return newEvent