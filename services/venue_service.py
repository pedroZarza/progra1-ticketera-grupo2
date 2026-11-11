from repositories import venue_repository
from datetime import datetime


def get_all_venues():
    return venue_repository.load_venues()


def get_active_venues():
    venues = venue_repository.load_venues()
    activeVenues = [venue for venue in venues if venue["active"]]
    print(activeVenues)
    return activeVenues
    
def get_venue_by_id(venueId):
    venues = venue_repository.load_venues()
    for venue in venues:
        if venue["id"] == venueId:
            return venue
    raise LookupError(f"No existe un venue con ID: {venueId}")



def create_venue(name, address, time_slots, sectors):
    venues = venue_repository.load_venues()
    for venue in venues:
        if venue["name"].lower() == name.lower():
            raise ValueError("Ya existe un venue con ese nombre.")
    if len(venues) > 0:
        newId = venues[-1]["id"] + 1
    else:
        newId = 1
    newVenue = {
        "id": newId,
        "name": name,
        "address": address,
        "active": True,
        "time_slots": time_slots,
        "sectors": sectors
    }
    venues.append(newVenue)
    venue_repository.save_venues(venues)
    return newVenue


def update_venue_by_id(venueId, newName, newAddress):
    venues = venue_repository.load_venues()
    for venue in venues:
        if venue["name"].lower() == newName.lower() and venue["id"] != venueId:
            raise ValueError("Ya existe otro venue con ese nombre.")

    for venue in venues:
        if venue["id"] == venueId:
            venue["name"] = newName
            venue["address"] = newAddress

            venue_repository.save_venues(venues)
            return venue
    raise LookupError(f"No existe un venue con ID: '{venueId}'")


def add_venue_time_slot(venueId, timeSlot):
    venues = venue_repository.load_venues()

    for venue in venues:
        if venue["id"] == venueId:
            if timeSlot in venue["time_slots"]:
                raise ValueError("El horario ingresado ya existe en el venue.")

            venue["time_slots"].append(timeSlot)
            venue_repository.save_venues(venues)
            return venue

    raise LookupError(f"No existe un venue con ID: '{venueId}'")


def remove_venue_time_slot(venueId, timeSlot):
    venues = venue_repository.load_venues()

    for venue in venues:
        if venue["id"] == venueId:
            if timeSlot not in venue["time_slots"]:
                raise ValueError("El horario ingresado no existe en el venue.")

            elif len(venue["time_slots"]) == 1:
                raise ValueError("No es posible eliminar. El venue debe tener al menos un horario.")

            venue["time_slots"].remove(timeSlot)
            venue_repository.save_venues(venues)
            return venue

    raise LookupError(f"No existe un venue con ID: '{venueId}'")



def add_venue_sector(venueId, sectorName, sectorData):
    venues = venue_repository.load_venues()
    for venue in venues:
        if venue["id"] == venueId:
            for existingName in venue["sectors"]:
                if existingName.lower() == sectorName.lower():
                    raise ValueError("Ya existe un sector con ese nombre.")

            venue["sectors"][sectorName] = sectorData
            venue_repository.save_venues(venues)
            return venue

    raise LookupError(f"No existe un venue con ID: {venueId}")


def remove_venue_sector(venueId, sectorName):
    venues = venue_repository.load_venues()

    for venue in venues:
        if venue["id"] == venueId:
            if sectorName not in venue["sectors"]:
                raise ValueError("El sector ingresado no existe en el venue.")

            if len(venue["sectors"]) == 1:
                raise ValueError("No es posible eliminar. El venue debe tener al menos un sector definido.")

            del venue["sectors"][sectorName]

            venue_repository.save_venues(venues)
            return venue

    raise LookupError(f"No existe un venue con ID: {venueId}")


def update_venue_sector(venueId, sectorName, sectorData):
    venues = venue_repository.load_venues()

    for venue in venues:
        if venue["id"] == venueId:
            if sectorName not in venue["sectors"]:
                raise ValueError("El sector ingresado no existe en el venue.")

            sector = venue["sectors"][sectorName]

            if sector["type"] == "general":
                sector.update({
                    "capacity": sectorData["capacity"]
                })

            elif sector["type"] == "numbered":
                sector.update({
                    "rows": sectorData["rows"],
                    "columns": sectorData["columns"]
                })

            venue_repository.save_venues(venues)
            return venue

    raise LookupError(f"No existe un venue con ID: {venueId}")








# def delete_venue(venue_id):
#     venues = get_all_venues()
#     for venue in venues:
#         if str(venue["id"]) == venue_id:
#             venues_data.venues.remove(venue)
#             return True

#     return False

# def deactivate_venue(venue_id):
#     for venue in venues_data.venues:
#         if str(venue["id"]) == venue_id:
#             venue["active"] = False
#             return True

#     return False






# def get_venue_statistics(venue_name):
#     total_occupancy = 0
#     total_events = 0
#     finished_events = 0
#     upcoming_events = 0

#     for event in events_data.events:
#         if event["venue"] == venue_name:
#             total_events += 1

#             event_date = datetime.fromisoformat(event["datetime"])

#             if event_date < datetime.now():
#                 finished_events += 1
#             else:
#                 upcoming_events += 1

#             capacity = 0
#             sold = 0

#             for sector in event["sectors"].values():
#                 if "capacity" in sector:
#                     capacity += sector["capacity"]
#                     sold += sector["sold"]
#                 else:
#                     for row in sector["seats"]:
#                         for seat in row:
#                             capacity += 1

#                             if seat == "occupied":
#                                 sold += 1

#             if capacity > 0:
#                 total_occupancy += sold * 100 / capacity

#     average_occupancy = 0

#     if total_events > 0:
#         average_occupancy = total_occupancy / total_events

#     return average_occupancy, finished_events, upcoming_events