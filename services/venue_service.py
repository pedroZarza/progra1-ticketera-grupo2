from data import venues_data
from data import events_data
from datetime import datetime


def get_venues():
    return venues_data.venues

def edit_venue(venue_id, new_name, new_address):
    for venue in venues_data.venues:
        if str(venue["id"]) == venue_id:
            venue["name"] = new_name
            venue["address"] = new_address
            return True

    return False


def delete_venue(venue_id):
    for venue in venues_data.venues:
        if str(venue["id"]) == venue_id:
            venues_data.venues.remove(venue)
            return True

    return False

def deactivate_venue(venue_id):
    for venue in venues_data.venues:
        if str(venue["id"]) == venue_id:
            venue["active"] = False
            return True

    return False

def create_venue(name, address, time_slots, sectors):
    for venue in venues_data.venues:
        if venue["name"].lower() == name.lower():
            return False

    new_id = 1

    for venue in venues_data.venues:
        if venue["id"] >= new_id:
            new_id = venue["id"] + 1

    new_venue = {
        "id": new_id,
        "name": name,
        "address": address,
        "active": True,
        "time_slots": time_slots,
        "sectors": sectors
    }

    venues_data.venues.append(new_venue)
    return True

def get_venue_statistics(venue_name):
    total_occupancy = 0
    total_events = 0
    finished_events = 0
    upcoming_events = 0

    for event in events_data.events:
        if event["venue"] == venue_name:
            total_events += 1

            event_date = datetime.fromisoformat(event["datetime"])

            if event_date < datetime.now():
                finished_events += 1
            else:
                upcoming_events += 1

            capacity = 0
            sold = 0

            for sector in event["sectors"].values():
                if "capacity" in sector:
                    capacity += sector["capacity"]
                    sold += sector["sold"]
                else:
                    for row in sector["seats"]:
                        for seat in row:
                            capacity += 1

                            if seat == "occupied":
                                sold += 1

            if capacity > 0:
                total_occupancy += sold * 100 / capacity

    average_occupancy = 0

    if total_events > 0:
        average_occupancy = total_occupancy / total_events

    return average_occupancy, finished_events, upcoming_events