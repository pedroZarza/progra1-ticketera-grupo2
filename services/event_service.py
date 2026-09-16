import uuid
from datetime import datetime
from data.events_data import events
from data.venues_data import venues 
from data.categories_data import categories 

def read_all_events():
    events.sort(key=lambda event: event["datetime"])
    return events

def create_event_service(organizerId, name, datetimeStr, category, venueIdStr, description):
    
    if not all(char.isalnum() or char.isspace() for char in name):
        raise ValueError("El nombre del evento no puede contener caracteres especiales. Solo se permiten letras, números y espacios.")

    if not all(char.isalnum() or char.isspace() for char in description):
        raise ValueError("La descripción del evento no puede contener caracteres especiales. Solo se permiten letras, números y espacios.")

    venue = next((v for v in venues if str(v["id"]) == str(venueIdStr)), None)
    if not venue:
        raise ValueError("El venue seleccionado no existe.")

    try:
        eventDate = datetime.strptime(datetimeStr, "%d/%m/%Y %H:%M")
        if eventDate < datetime.now():
            raise ValueError("La fecha del evento no puede ser en el pasado.")
        
        isoDatetime = eventDate.isoformat() 
    except ValueError as e:
        if "does not match format" in str(e):
            raise ValueError("Formato de fecha inválido. Utilice DD/MM/AAAA HH:MM.")
        raise e

    eventTimeStr = eventDate.strftime("%H:%M")
    if eventTimeStr not in venue.get("time_slots", []):
        raise ValueError(f"El horario {eventTimeStr} no está disponible para este venue. Opciones: {', '.join(venue['time_slots'])}")

    for event in events:
        is_same_venue = str(event.get("venueId")) == str(venue["id"]) or event.get("venue") == venue.get("name")
        
        is_same_time = False
        if event.get("datetime"):
            existing_dt = datetime.fromisoformat(event.get("datetime"))
            if existing_dt == eventDate:
                is_same_time = True
                
        if is_same_venue and is_same_time and event.get("state") != "canceled":
            raise ValueError("El venue ya tiene un evento programado para esa misma fecha y horario.")

    matchedCategory = next((c for c in categories if c.lower() == category.lower()), None)
    if not matchedCategory:
        raise ValueError(f"Categoría inexistente. Opciones válidas: {', '.join(categories)}")

    newEvent = {
        "id": str(uuid.uuid4()), 
        "organizerId": organizerId,
        "name": name,
        "datetime": isoDatetime, 
        "category": matchedCategory, 
        "categories": [matchedCategory],
        "venueId": venue["id"], 
        "venue": venue.get("name", f"Venue {venue['id']}"), 
        "description": description,
        "state": "active",
        "sectorPrices": {sectorName: None for sectorName in venue.get("sectors", {}).keys()}
    }
    
    events.append(newEvent)
    
    return newEvent

def get_events_by_organizer_service(organizerId):
    
    organizerEvents = [event for event in events if str(event.get("organizerId")) == str(organizerId)]
    organizerEvents.sort(key=lambda e: e.get("datetime", ""))
    
    return organizerEvents

def search_organizer_events_by_name_service(search_term, organizerId):
    
    my_events = get_events_by_organizer_service(organizerId)
    
    # --- ACÁ ESTÁ EL CAMBIO ---
    found_events = [
        event for event in my_events 
        if search_term.lower() == event.get("name", "").lower()
    ]
    
    return found_events