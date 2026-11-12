from repositories import event_repository, venue_repository


def get_all_venues():
    """Devuelve todos los venues.

    Retorna:
        list: venues registrados.
    """
    return venue_repository.load_venues()


def get_active_venues():
    """Devuelve solo los venues activos.

    Retorna:
        list: venues activos.
    """
    venues = venue_repository.load_venues()
    activeVenues = [venue for venue in venues if venue["active"]]
    return activeVenues

def get_deactive_venues():
    """Devuelve los venues inactivos.

    Retorna:
        list: venues inactivos.
    """
    venues = venue_repository.load_venues()
    deactiveVenues = [venue for venue in venues if not venue["active"]]
    return deactiveVenues



def get_venue_by_id(venueId):
    """Busca un venue por ID.

    Parámetros:
        venueId (int): identificador del venue.

    Retorna:
        dict: el venue encontrado.
    """
    venues = venue_repository.load_venues()
    for venue in venues:
        if venue["id"] == venueId:
            return venue
    raise LookupError(f"No existe un venue con ID: {venueId}")



def create_venue(name, address, time_slots, sectors):
    """Registra un venue con horarios y sectores.

    Parámetros:
        name (str): nombre del venue.
        address (str): dirección.
        time_slots (list): horarios en formato HH:MM.
        sectors (dict): sectores generales o numerados.

    Retorna:
        dict: el venue creado.
    """
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
    """Actualiza el nombre y la dirección de un venue.

    Parámetros:
        venueId (int): identificador del venue.
        newName (str): nuevo nombre.
        newAddress (str): nueva dirección.

    Retorna:
        dict: el venue actualizado.
    """
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
    """Agrega un horario al venue.

    Parámetros:
        venueId (int): identificador del venue.
        timeSlot (str): horario en formato HH:MM.

    Retorna:
        dict: el venue actualizado.
    """
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
    """Elimina un horario del venue, dejando al menos uno.

    Parámetros:
        venueId (int): identificador del venue.
        timeSlot (str): horario a eliminar.

    Retorna:
        dict: el venue actualizado.
    """
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
    """Agrega un sector al venue.

    Parámetros:
        venueId (int): identificador del venue.
        sectorName (str): nombre del sector.
        sectorData (dict): tipo y capacidad, o filas y columnas.

    Retorna:
        dict: el venue actualizado.
    """
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
    """Elimina un sector del venue, dejando al menos uno.

    Parámetros:
        venueId (int): identificador del venue.
        sectorName (str): nombre del sector.

    Retorna:
        dict: el venue actualizado.
    """
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
    """Actualiza la capacidad o la grilla de un sector.

    Parámetros:
        venueId (int): identificador del venue.
        sectorName (str): nombre del sector.
        sectorData (dict): nuevos datos del sector.

    Retorna:
        dict: el venue actualizado.
    """
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



def deactivate_venue(venueId):
    """Marca un venue como inactivo.

    Parámetros:
        venueId (int): identificador del venue.

    Retorna:
        dict: el venue inactivado.
    """
    venues = venue_repository.load_venues()

    for venue in venues:
        if venue["id"] == venueId:
            if venue["active"] == False:
                raise ValueError("No es posible inactivar. El venue ya se encuentra inactivo.")

            venue["active"] = False
            venue_repository.save_venues(venues)
            return venue

    raise LookupError(f"No existe un venue con ID: {venueId}")

def activate_venue(venueId):
    """Marca un venue como activo.

    Parámetros:
        venueId (int): identificador del venue.

    Retorna:
        dict: el venue activado.
    """
    venues = venue_repository.load_venues()
    for venue in venues:
        if venue["id"] == venueId:
            if venue["active"] == True:
                raise ValueError("No es posible activar. El venue ya se encuentra activo.")
            venue["active"] = True
            venue_repository.save_venues(venues)
            return venue
    raise LookupError(f"No existe un venue con ID: {venueId}")


def delete_venue(venueId):
    """Elimina un venue que no tenga eventos asociados.

    Parámetros:
        venueId (int): identificador del venue.

    Retorna:
        dict: el venue eliminado.
    """
    venues = venue_repository.load_venues()
    events = event_repository.load_events()

    for venue in venues:
        if venue["id"] == venueId:
            for event in events:
                if event["venueId"] == venueId:
                    raise ValueError("No es posible eliminar. El venue tiene eventos asociados.")

            venues.remove(venue)
            venue_repository.save_venues(venues)
            return venue

    raise LookupError(f"No existe un venue con ID: {venueId}")
