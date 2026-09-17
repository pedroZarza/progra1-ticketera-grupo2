from datetime import datetime
from data.events_data import events
from data.venues_data import venues 
from data.categories_data import categories 



def read_all_events():
    events.sort(key=lambda event: event["datetime"])
    return events

def read_active_events():
    activeEvents = list(filter(lambda event: event["status"] == "active" and has_availability(event),events))
    activeEvents.sort(key=lambda event: event["datetime"])
    return activeEvents

def has_availability(event):
    for sector in event["sectors"].values():
        if "capacity" in sector and sector["sold"] < sector["capacity"]:
            return True

        if "seats" in sector:
            for row in sector["seats"]:
                if "free" in row:
                    return True
    return False

def get_event_by_id(event_id):
    for event in events:
        if str(event["id"]) == event_id:
            return event
    return None

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
        eventId = events[-1]["id"] + 1 
    else:
        eventId = 1       
        
    newEvent = {
        "id": eventId,
        "organizerId": organizerId,
        "name": name,
        "datetime": isoDatetime, 
        "category": matchedCategory, 
        "categories": [matchedCategory],
        "venueId": venue["id"], 
        "venue": venue.get("name", f"Venue {venue['id']}"), 
        "description": description,
        "state": "active",
        "sectors": eventSectors
    }
    
    events.append(newEvent)
    
    return newEvent

def get_events_by_organizer_service(organizerId):
    
    organizerEvents = [event for event in events if str(event.get("organizerId")) == str(organizerId)]
    organizerEvents.sort(key=lambda e: e.get("datetime", ""))
    
    return organizerEvents

def search_organizer_events_by_name_service(search_term, organizerId):
    
    my_events = get_events_by_organizer_service(organizerId)
    
    found_events = [
        event for event in my_events 
        if search_term.lower() == event.get("name", "").lower()
    ]
    
    return found_events

def search_organizer_events_by_category_service(category_term, organizerId):
    
    my_events = get_events_by_organizer_service(organizerId)
    term = category_term.lower().strip()
    
    found_events = []
    for event in my_events:
        event_categories = [str(c).lower() for c in event.get("categories", [])]
        singular_category = str(event.get("category", "")).lower()
        match_in_list = any(term in cat for cat in event_categories)
        match_in_singular = term in singular_category
        
        if match_in_list or match_in_singular:
            found_events.append(event)
            
    return found_events

def update_event_service(organizerId, eventId, name=None, description=None, category=None):
    my_events = get_events_by_organizer_service(organizerId)
    
    matching_events = [
        e for e in my_events 
        if str(e.get("id")) == str(eventId) or str(e.get("id")).startswith(str(eventId))
    ]
    
    if not matching_events:
        raise ValueError("El evento no existe o no tenés permisos para modificarlo.")
        
    if len(matching_events) > 1:
        raise ValueError("Se encontraron múltiples eventos con ese prefijo de ID. Por favor, ingrese más caracteres para ser específico.")
        
    event = matching_events[0]
    validated_name = None
    validated_desc = None
    validated_cat = None
    
    if name is not None and name.strip() != "":
        if not all(char.isalnum() or char.isspace() for char in name):
            raise ValueError("El nombre del evento no puede contener caracteres especiales.")
        validated_name = name
        
    if description is not None and description.strip() != "":
        if not all(char.isalnum() or char.isspace() for char in description):
            raise ValueError("La descripción no puede contener caracteres especiales.")
        validated_desc = description
        
    if category is not None and category.strip() != "":
        matchedCategory = next((c for c in categories if c.lower() == category.lower()), None)
        if not matchedCategory:
            raise ValueError(f"Categoría inexistente. Opciones válidas: {', '.join(categories)}")
        validated_cat = matchedCategory

    if validated_name is not None:
        event["name"] = validated_name
        
    if validated_desc is not None:
        event["description"] = validated_desc
        
    if validated_cat is not None:
        event["category"] = validated_cat
        event["categories"] = [validated_cat]
        
    return event
        
def get_organizer_event_by_id_service(organizerId, eventId):
    for event in events:
        same_organizer = str(event.get("organizerId")) == str(organizerId)
        same_event = str(event.get("id"))[:8] == str(eventId)

        if same_organizer and same_event:
            return event

    return None
def update_event_prices_service(organizerId, eventId, prices):
    event = get_organizer_event_by_id_service(organizerId, eventId)

    if event is None:
        raise ValueError("El evento no existe o no pertenece al organizador.")

    if "sectors" not in event:
        raise ValueError("El evento no tiene sectores configurados.")

    for sectorName, price in prices.items():

        if sectorName not in event["sectors"]:
            raise ValueError(f"El sector {sectorName} no existe.")

        if price <= 0:
            raise ValueError("El precio debe ser mayor a cero.")

        event["sectors"][sectorName]["price"] = price

    return event

def get_event_sales_status_service(organizerId, eventId):

    event = get_organizer_event_by_id_service(organizerId, eventId)

    if event is None:
        raise ValueError("El evento no existe o no pertenece al organizador.")

    if "sectors" not in event:
        raise ValueError("El evento no tiene sectores configurados.")

    sectorStats = []

    totalCapacity = 0
    totalSold = 0
    totalAvailable = 0

    for sectorName, sectorData in event["sectors"].items():

        if "capacity" in sectorData:
            capacity = sectorData["capacity"]
            sold = sectorData["sold"]
            available = capacity - sold

        elif "seats" in sectorData:
            capacity = 0
            available = 0

            for row in sectorData["seats"]:
                for seat in row:
                    capacity += 1

                    if seat == "free":
                        available += 1

            sold = capacity - available

        else:
            capacity = 0
            sold = 0
            available = 0

        if capacity > 0:
            occupancy = (sold * 100) / capacity
        else:
            occupancy = 0

        sectorStats.append({
            "name": sectorName,
            "capacity": capacity,
            "sold": sold,
            "available": available,
            "occupancy": occupancy
        })

        totalCapacity += capacity
        totalSold += sold
        totalAvailable += available

    if totalCapacity > 0:
        totalOccupancy = (totalSold * 100) / totalCapacity
    else:
        totalOccupancy = 0

    return {
        "event": event,
        "sectors": sectorStats,
        "totalCapacity": totalCapacity,
        "totalSold": totalSold,
        "totalAvailable": totalAvailable,
        "totalOccupancy": totalOccupancy
    }
def assign_category_service(organizerId, eventId, category):
   
    my_events = get_events_by_organizer_service(organizerId)
    
    matching_events = [
        e for e in my_events 
        if str(e.get("id")) == str(eventId) or str(e.get("id")).startswith(str(eventId))
    ]
    
    if not matching_events:
        raise ValueError("El evento no existe o no tenés permisos para modificarlo.")
        
    if len(matching_events) > 1:
        raise ValueError("Se encontraron múltiples eventos con ese prefijo de ID. Por favor, ingrese más caracteres para ser específico.")
        
    event = matching_events[0]
    
    if not category:
        raise ValueError("Debe ingresar una categoría válida.")
        
    matchedCategory = next((c for c in categories if c.lower() == category.lower()), None)
    if not matchedCategory:
        raise ValueError(f"Categoría inexistente. Opciones válidas: {', '.join(categories)}")
        
    event["category"] = matchedCategory
    event["categories"] = [matchedCategory]
    
    return event
