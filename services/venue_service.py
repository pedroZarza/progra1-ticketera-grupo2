from data import venues_data


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