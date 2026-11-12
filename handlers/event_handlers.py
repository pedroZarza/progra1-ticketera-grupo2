from services import event_service, user_service, category_service, venue_service
from utils import layout_helpers
from utils import input_helpers
from utils.messages import show_error, show_info, show_success

def show_events():
    events = event_service.get_active_events()
    if len(events) == 0:
        show_info("No hay eventos disponibles.")
        input("\nPresiona ENTER para volver al menú principal...")
        return  
    layout_helpers.events_board(events)
    input("\nPresiona ENTER para volver al menú principal...")
    return

def show_event_detail():
    operationSuccess = False
    events = event_service.get_active_events()
    if len(events) == 0:
        show_info("No hay eventos disponibles.")
        input("\nPresiona ENTER para volver al menú principal...")
        return    
    layout_helpers.events_board(events)
    while not operationSuccess:
        eventId = input_helpers.prompt_positive_number("\nIngrese el ID del evento que desea ver: ")
        if eventId == "q":
            return
        try:
            event = event_service.get_event_by_id(eventId)
            organizer = user_service.get_user_by_id(event["organizerId"])
            layout_helpers.event_detail(event, organizer)
            operationSuccess = True        
        except LookupError as error:
            show_error(error)
            response = input("\nPresiona ENTER para volver a intentar o q para cancelar la operación...")
            if response.lower() == "q": return
    input("\nPresiona ENTER para volver al menú principal...")
    return

def search_events():
    operationSuccess = False
    while not operationSuccess:
        query = input_helpers.prompt_non_empty_field("Búsqueda: ")
        if query== "q":
            return
        results = event_service.get_events_by_search(query)
        if len(results) == 0:
            show_info("No se encontraron eventos que coicidan con su búsqueda.")
        else:
            layout_helpers.events_board(results)
        response = input("\nPresiona ENTER para volver a buscar o q para cancelar la operación...")
        if response.lower() == "q": operationSuccess = True
    return 


def filter_events_by_category():
    categories = category_service.get_categories()
    if len(categories) == 0:
        show_info("No hay categorías disponibles.")
        input("\nPresiona ENTER para volver al menú principal...")
        return
    print("\nCategorías disponibles:")
    for category in categories:
        print(f"- {category}")
        
    operationSuccess = False
    while not operationSuccess:
        categoriesQuery = input_helpers.prompt_non_empty_field(
            "\nIngrese las categorías, separadas por comas (q para cancelar): "
        )
        if categoriesQuery.lower() == "q":
            return
        selectedCategories = [
            category.strip().lower()
            for category in categoriesQuery.split(",")
            if category.strip() != ""
        ]

        results = event_service.get_events_by_category(selectedCategories)

        if len(results) == 0:
            show_info("No se encontraron eventos con las categorías ingresadas.")
        else:
            layout_helpers.events_board(results)
            response = input("\nPresiona ENTER para volver a buscar o q para cancelar la operación...")
            if response.lower() == "q": operationSuccess = True
    return



def create_new_event(user):
    print("\n- CREAR NUEVO EVENTO -")
    venues = venue_service.get_active_venues()
    categories = category_service.get_categories()

    operationSuccess = False
    while not operationSuccess:
        name = input_helpers.prompt_non_empty_field("\nNombre del evento: ")
        if name.lower() == "q": return

        description = input_helpers.prompt_non_empty_field("\nDescripción: ")
        if description.lower() == "q": return

        scheduleSelected = False
        while not scheduleSelected:

            print("\nVenues activos:")
            if len(venues) == 0:
                show_info("No hay venues activos disponibles.")
                input("\nPresiona ENTER para volver al menú principal...")
                return
            for venue in venues:
                print(f"[{venue['id']}] {venue['name']}")
            
            venueId = input_helpers.prompt_positive_number("\nSeleccione el venue mediante su id: ")
            if venueId == "q": return

            date = input_helpers.prompt_date("\nFecha (DD/MM/AAAA): ")
            if date.lower() == "q": return

            try:
                availableSlots = event_service.get_available_time_slots(venueId, date)
            except (ValueError, LookupError) as error:
                show_error(error)
                response = input("\nPresiona ENTER para volver a intentar o q para cancelar la operación...")
                if response.strip().lower() == "q":
                    return
                continue

            print("\nHorarios disponibles:")
            for index, slot in enumerate(availableSlots, start=1):
                print(f"{index}. {slot}")

            time = input_helpers.prompt_list_option("\nSeleccione un horario: ", availableSlots)
            if time.lower() == "q": return
            scheduleSelected = True

        print("\nCategorías disponibles:")
        if len(categories) == 0:
            show_info("No hay categorías disponibles.") 
            input("\nPresiona ENTER para volver al menú principal...")
            return
        for index, category in enumerate(categories, start=1):
            print(f"{index}. {category}")

        selectedCategories = []
        while True:
            category = input_helpers.prompt_list_option("\nIngrese las categorías del evento (q para terminar selección): ", categories)
            if category == "q":
                if len(selectedCategories) == 0:
                    show_error("Debe seleccionar al menos una categoría.")
                    continue
                break
            if category in selectedCategories:
                show_error("Esa categoría ya fue agregada.")
                continue
            selectedCategories.append(category)
            show_success(f"Categoría '{category}' agregada correctamente.")
        try:
            event = event_service.create_event(
                user["id"], name, description, date, time, selectedCategories, venueId
            )
            show_success("El evento ha sido dado de alta con éxito.")
            print(f"\n[{event['id']}] {event['name']}")
            operationSuccess = True
        except (ValueError, LookupError) as error:
            show_error(error)
            response = input("\nPresiona ENTER para volver a intentar o q para cancelar la operación...")
            if response.strip().lower() == "q":
                return
    define_event_prices(event["id"], required=True)
    input("\nPresiona ENTER para volver al menú principal...")



def define_event_prices(eventId, required=False):
    print("\n- DEFINIR/MODIFICAR PRECIOS -")
    try:
        event = event_service.get_event_by_id(eventId)
    except LookupError as error:
        show_error(error)
        input("\nPresiona ENTER para volver al menú principal...")
        return

    print(f"\n[{event['id']}] {event['name']}")
    print("-" * 45)

    sectorPrices = []
    for i, (sectorName, sectorData) in enumerate(event["sectors"].items(), start=1):
        priceAccepted = False
        while not priceAccepted:
            if "capacity" in sectorData:
                print(f"\nSector {i}: '{sectorName}' (capacity: {sectorData['capacity']})")
            else:
                capacity = len(sectorData["seats"]) * len(sectorData["seats"][0])
                print(f"\nSector {i}: '{sectorName}' (capacity: {capacity})")


            print(f"Precio: ${sectorData['price']:.2f}" if sectorData['price'] is not None else "Precio: No definido")
            price = input_helpers.prompt_price("\nIngrese el nuevo precio del sector: ")
            if price == "q":
                if required:
                    show_error("Debe definir el precio de todos los sectores.")
                    continue
                show_info("Operación cancelada. No se guardaron los precios.")
                input("\nPresiona ENTER para volver al menú principal...")  
                return

            sectorPrices.append((sectorName, price))
            priceAccepted = True

    try:
        for sectorName, price in sectorPrices:
            event_service.update_sector_price(eventId, sectorName, price)
        show_success("Los precios de los sectores fueron actualizados.")
    except (LookupError, ValueError) as error:
        show_error(error)
        input("\nPresiona ENTER para volver al menú principal...")


def view_my_events(user):
    events = event_service.get_events_by_organizer(user["id"])
    layout_helpers.organizer_events_board(events)
    input("\nPresiona ENTER para volver al menú principal...")


def show_organizer_event_detail(user):
    operationSuccess = False
    events = event_service.get_events_by_organizer(user["id"])
    if len(events) == 0:
        show_info("No tenés eventos publicados.")
        input("\nPresiona ENTER para volver al menú principal...")
        return
    layout_helpers.organizer_events_board(events)
    while not operationSuccess:
        eventId = input_helpers.prompt_positive_number("\nIngrese el ID del evento que desea ver: ")
        if eventId == "q":
            return
        try:
            event = event_service.get_event_by_organizer(user["id"], eventId)
            layout_helpers.event_detail(event, user)
            operationSuccess = True
        except LookupError as error:
            show_error(error)
            response = input("\nPresiona ENTER para volver a intentar o q para cancelar la operación...")
            if response.lower() == "q": return
    input("\nPresiona ENTER para volver al menú principal...")


def assign_event_category(user):
    print("\n- ASIGNAR CATEGORÍA A UN EVENTO -")
    events = event_service.get_events_by_organizer(user["id"])
    layout_helpers.organizer_events_board(events)
    if len(events) == 0:
        input("\nPresiona ENTER para volver al menú principal...")
        return

    while True:
        eventId = input_helpers.prompt_positive_number("\nIngrese el ID del evento: ")
        if eventId == "q":
            return

        selectedEvent = None
        for event in events:
            if event["id"] == eventId:
                selectedEvent = event
                break

        if selectedEvent is None:
            show_error("Ese evento no está en tu lista.")
            continue
        break

    catalog = category_service.get_categories()
    availableCategories = []
    for category in catalog:
        alreadyAssigned = False
        for assignedCategory in selectedEvent["categories"]:
            if assignedCategory.lower() == category.lower():
                alreadyAssigned = True
                break
        if not alreadyAssigned:
            availableCategories.append(category)

    if len(availableCategories) == 0:
        show_info("El evento ya tiene todas las categorías disponibles.")
        input("\nPresiona ENTER para volver al menú principal...")
        return

    print(f"\n[{selectedEvent['id']}] {selectedEvent['name']}")
    print("Categorías actuales:")
    for category in selectedEvent["categories"]:
        print(f"- {category}")

    print("\nCategorías disponibles:")
    for index, category in enumerate(availableCategories, start=1):
        print(f"{index}. {category}")

    category = input_helpers.prompt_list_option("\nSeleccione la categoría a asignar: ", availableCategories)
    if category == "q":
        return

    try:
        event_service.add_event_category(selectedEvent["id"], category)
        show_success(f"Categoría '{category}' asignada al evento.")
    except (ValueError, LookupError) as error:
        show_error(error)

    input("\nPresiona ENTER para volver al menú principal...")


def remove_event_category(user):
    print("\n- ELIMINAR CATEGORÍA DE UN EVENTO -")
    events = event_service.get_events_by_organizer(user["id"])
    layout_helpers.organizer_events_board(events)
    if len(events) == 0:
        input("\nPresiona ENTER para volver al menú principal...")
        return

    while True:
        eventId = input_helpers.prompt_positive_number("\nIngrese el ID del evento: ")
        if eventId == "q":
            return

        selectedEvent = None
        for event in events:
            if event["id"] == eventId:
                selectedEvent = event
                break

        if selectedEvent is None:
            show_error("El evento ingresado no está en tu lista.")
            continue
        break

    if len(selectedEvent["categories"]) == 1:
        show_error("El evento debe conservar al menos una categoría.")
        input("\nPresiona ENTER para volver al menú principal...")
        return

    print(f"\n[{selectedEvent['id']}] {selectedEvent['name']}")
    print("Categorías del evento:")
    for index, category in enumerate(selectedEvent["categories"], start=1):
        print(f"{index}. {category}")

    category = input_helpers.prompt_list_option("\nSeleccione la categoría a eliminar: ", selectedEvent["categories"])
    if category == "q":
        return

    try:
        event_service.remove_event_category(selectedEvent["id"], category)
        show_success(f"Categoría '{category}' eliminada del evento.")
    except (ValueError, LookupError) as error:
        show_error(error)

    input("\nPresiona ENTER para volver al menú principal...")


def edit_event_info(user):
    operationSuccess = False
    events = event_service.get_events_by_organizer(user["id"])
    if len(events) == 0:
        show_info("No tenés eventos publicados.")
        input("\nPresiona ENTER para volver al menú principal...")
        return

    layout_helpers.organizer_events_board(events)

    while not operationSuccess:
        eventId = input_helpers.prompt_positive_number("\nIngrese el ID del evento que desea editar: ")
        if eventId == "q": return

        newName = input_helpers.prompt_non_empty_field("\nIngrese el nuevo nombre: ")
        if newName.lower() == "q": return

        newDescription = input_helpers.prompt_non_empty_field("\nIngrese la nueva descripción: ")
        if newDescription.lower() == "q": return

        try:
            event_service.update_event_info(eventId, user["id"], newName, newDescription)
            show_success("Evento editado exitosamente.")
            operationSuccess = True
        except (ValueError, LookupError, PermissionError) as error:
            show_error(error)
            response = input("\nPresiona ENTER para volver a intentar o q para cancelar la operación...")
            if response.strip().lower() == "q": return
    input("\nPresiona ENTER para volver al menú principal...")


def edit_event_prices(user):
    print("\n- EDITAR PRECIOS DE UN EVENTO -")
    events = event_service.get_events_by_organizer(user["id"])
    layout_helpers.organizer_events_board(events)
    if len(events) == 0:
        input("\nPresiona ENTER para volver al menú principal...")
        return
    while True:
        eventId = input_helpers.prompt_positive_number("\nIngrese el ID del evento: ")
        if eventId == "q":
            return

        selectedEvent = None
        for event in events:
            if event["id"] == eventId:
                selectedEvent = event
                break

        if selectedEvent is None:
            show_error("El evento ingresado no está en tu lista.")
            continue

        define_event_prices(selectedEvent["id"])
        break

    input("\nPresiona ENTER para volver al menú principal...")


def cancel_event(user):
    operationSuccess = False
    events = event_service.get_events_by_organizer(user["id"])
    if len(events) == 0:
        show_info("No tenés eventos publicados.")
        input("\nPresiona ENTER para volver al menú principal...")
        return

    layout_helpers.organizer_events_board(events)

    while not operationSuccess:
        eventId = input_helpers.prompt_positive_number("\nIngrese el ID del evento que desea cancelar: ")
        if eventId == "q": return

        try:
            event_service.cancel_event(eventId, user["id"])
            show_success("Evento cancelado exitosamente.")
            operationSuccess = True
        except (ValueError, LookupError, PermissionError) as error:
            show_error(error)
            response = input("\nPresiona ENTER para volver a intentar o q para cancelar la operación...")
            if response.strip().lower() == "q": return
    input("\nPresiona ENTER para volver al menú principal...")



def view_event_history(user):
    events = event_service.get_events_history(user["id"])
    if len(events) == 0:
        show_info("No tenés eventos en el historial.")
        input("\nPresiona ENTER para volver al menú principal...")
        return
    print("\nHISTORIAL DE EVENTOS:")
    layout_helpers.organizer_events_board(events)
    input("\nPresiona ENTER para volver al menú principal...")
    return



def view_event_orders(user):
    events = event_service.get_events_by_organizer(user["id"])
    if len(events) == 0:
        show_info("No tenés eventos publicados.")
        input("\nPresiona ENTER para volver al menú principal...")
        return
    layout_helpers.organizer_events_board(events)
    operationSuccess = False
    while not operationSuccess:
        eventId = input_helpers.prompt_positive_number("\nIngrese el ID del evento que desea consultar: ")
        if eventId == "q":
            return
        try:
            orders = event_service.get_event_orders(eventId)
            event = event_service.get_event_by_id(eventId)
            layout_helpers.event_orders(event, orders)
            operationSuccess = True        
        except LookupError as error:
            show_error(error)
            response = input("\nPresiona ENTER para volver a intentar o q para cancelar la operación...")
            if response.lower() == "q": return
    input("\nPresiona ENTER para volver al menú principal...")
    return

def view_event_sales_summary(user):
    events = event_service.get_all_events_by_organizer(user["id"])
    if len(events) == 0:
        show_info("No tenés eventos publicados.")
        input("\nPresiona ENTER para volver al menú principal...")
        return
    layout_helpers.organizer_events_board(events)
    operationSuccess = False
    while not operationSuccess:
        eventId = input_helpers.prompt_positive_number("\nIngrese el ID del evento que desea consultar: ")
        if eventId == "q":
            return
        try:
            event = event_service.get_any_event_by_organizer(user["id"], eventId)
            layout_helpers.event_status_summary(event)
            operationSuccess = True
        except LookupError as error:
            show_error(error)
            response = input("\nPresiona ENTER para volver a intentar o q para cancelar la operación...")
            if response.lower() == "q":
                return
    input("\nPresiona ENTER para volver al menú principal...")



