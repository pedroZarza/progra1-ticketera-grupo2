from services import event_service, user_service, category_service, venue_service
from utils import layout_helpers
from utils import input_helpers
from utils.messages import show_error, show_info, show_success

def show_events():
    events = event_service.get_active_events()
    if len(events) == 0:
        show_info("No hay eventos disponibles.")
        return  
    layout_helpers.events_board(events)
    input("\nPresiona ENTER para volver al menú principal...")
    return

def show_event_detail():
    operationSuccess = False
    events = event_service.get_active_events()
    if len(events) == 0:
        show_info("No hay eventos disponibles.")
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
                return

            sectorPrices.append((sectorName, price))
            priceAccepted = True

    try:
        for sectorName, price in sectorPrices:
            event_service.update_sector_price(eventId, sectorName, price)
        show_success("Los precios de los sectores fueron actualizados.")
    except (LookupError, ValueError) as error:
        show_error(error)


def edit_event_prices(user):
    print("\n- EDITAR PRECIOS DE UN EVENTO -")
    events = event_service.get_events_by_organizer(user["id"])
    if len(events) == 0:
        show_info("No tenés eventos disponibles para editar.")
        return

    layout_helpers.events_board(events)
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

        define_event_prices(selectedEvent["id"])
        break

    input("\nPresiona ENTER para volver al menú principal...")
    
            
    

# def view_my_events(organizerId):
#     pass
    
#     print("\n" + "="*55)
#     print("              MIS EVENTOS PUBLICADOS".center(55))
#     print("="*55)
    
#     myEvents = service.get_events_by_organizer_service(organizerId)
    
#     if not myEvents:
#         print("\n[INFO] Todavía no tenés ningún evento publicado.")
#     else:
#         layout_helpers.events_board(myEvents)
            
#     input("\nPresiona ENTER para volver al menú principal...")
#     return

# def search_event_by_name(organizerId):
#     pass
    
#     print("\n" + "="*55)
#     print("              BUSCAR EVENTO POR NOMBRE".center(55))
#     print("="*55)
    
#     search_term = input("Ingrese el nombre exacto del evento a buscar: ").strip()
    
#     if not search_term:
#         print("\n[ADVERTENCIA] No ingresaste ningún texto de búsqueda.")
#         input("\nPresiona ENTER para volver al menú...")
#         return
        
#     results = service.search_organizer_events_by_name_service(search_term, organizerId)
    
#     if not results:
#         print(f"\n[INFO] No se encontró ningún evento que se llame exactamente '{search_term}'.")
#     else:
#         print(f"\n[INFO] Evento encontrado:")
#         layout_helpers.events_board(results)
        
#     input("\nPresiona ENTER para volver al menú principal...")
#     return

# def search_event_by_category(organizerId):
#     pass
    
#     print("\n" + "="*55)
#     print("            BUSCAR EVENTO POR CATEGORÍA".center(55))
#     print("="*55)
    
#     availableCategories = ", ".join(categories)
#     category = input(f"Ingrese la categoría a buscar ({availableCategories}): ").strip()
    
#     if not category:
#         print("\n[ADVERTENCIA] No ingresaste ninguna categoría.")
#         input("\nPresiona ENTER para volver al menú...")
#         return
        
#     results = service.search_organizer_events_by_category_service(category, organizerId)
    
#     if not results:
#         print(f"\n[INFO] No tenés eventos registrados en la categoría '{category}'.")
#     else:
#         print(f"\n[INFO] Se encontraron {len(results)} evento(s) de {category.capitalize()}:")
#         layout_helpers.events_board(results)
        
#     input("\nPresiona ENTER para volver al menú principal...")
#     return

# def edit_event(organizerId):
#     print("\n" + "="*55)
#     print("                 MODIFICAR EVENTO".center(55))
#     print("="*55)
    
#     myEvents = service.get_events_by_organizer_service(organizerId)
#     if not myEvents:
#         print("\n[INFO] No tenés ningún evento publicado para modificar.")
#         input("\nPresiona ENTER para volver al menú...")
#         return
        
#     layout_helpers.events_board(myEvents)
    
#     eventId = input("\nIngrese el ID (o los primeros caracteres) del evento a modificar: ").strip()
#     if not eventId:
#         print("\n[ADVERTENCIA] Operación cancelada.")
#         input("\nPresiona ENTER para volver...")
#         return
        
#     matching_events = [
#         e for e in myEvents 
#         if str(e.get("id")) == str(eventId) or str(e.get("id")).startswith(str(eventId))
#     ]
    
#     if not matching_events:
#         print("\n[ERROR] No se encontró ningún evento tuyo con ese ID.")
#         input("\nPresiona ENTER para volver...")
#         return
        
#     if len(matching_events) > 1:
#         print("\n[ERROR] Hay varios eventos que coinciden con ese prefijo de ID.")
#         print("Por favor, ingrese más caracteres del ID para identificarlo inequívocamente.")
#         input("\nPresiona ENTER para volver...")
#         return
        
#     target_event = matching_events[0]
    
#     print(f"\n[INFO] Modificando: '{target_event['name']}'")
#     print("Deje el campo en blanco y presione ENTER si no desea modificarlo.\n")
    
#     new_name = input(f"Nuevo nombre [{target_event['name']}]: ").strip()
#     new_desc = input(f"Nueva descripción [{target_event.get('description', '')}]: ").strip()
    
#     availableCategories = ", ".join(categories)
#     current_cat = ""
#     if len(target_event.get("categories", [])) > 0:
#         current_cat = target_event["categories"][0]
#     new_cat = input(f"Nueva categoría ({availableCategories}) [{current_cat}]: ").strip()
    
#     try:
#         service.update_event_service(
#             organizerId=organizerId,
#             eventId=target_event["id"],
#             name=new_name if new_name else None,
#             description=new_desc if new_desc else None,
#             category=new_cat if new_cat else None
#         )
#         print("\n" + "-"*45)
#         print("¡El evento fue modificado exitosamente!")
#         print("-" * 45)
#     except ValueError as e:
#         print(f"\n[ADVERTENCIA] {e}")
#     except Exception as e:
#         print(f"\n[ERROR CRÍTICO] Ocurrió un error inesperado: {e}")
        
#     input("\nPresiona ENTER para volver al menú principal...")
#     return
# def define_event_prices(organizerId):
#     pass

#     print("\n" + "="*55)
#     print("            DEFINIR PRECIOS POR SECTOR".center(55))
#     print("="*55)

#     myEvents = service.get_events_by_organizer_service(organizerId)

#     if not myEvents:
#         print("\n[INFO] Todavía no tenés eventos publicados.")
#         input("\nPresiona ENTER para volver al menú...")
#         return

#     layout_helpers.events_board(myEvents)

#     eventId = input("\nIngrese el ID del evento: ").strip()

#     event = service.get_organizer_event_by_id_service(organizerId, eventId)

#     if event is None:
#         print("\n[ERROR] El evento no existe o no pertenece a tu usuario.")
#         input("\nPresiona ENTER para volver al menú...")
#         return

#     prices = {}

#     for sectorName, sectorData in event["sectors"].items():

#         currentPrice = sectorData["price"]

#         print(f"\nSector: {sectorName}")

#         if currentPrice is None:
#             print("Precio actual: sin definir")
#         else:
#             print(f"Precio actual: ${currentPrice}")

#         while True:
#             priceStr = input("Ingrese el nuevo precio: ").strip()

#             if not priceStr.isdigit():
#                 print("[ERROR] El precio debe ser un número entero.")
#                 continue

#             price = int(priceStr)

#             if price <= 0:
#                 print("[ERROR] El precio debe ser mayor a cero.")
#                 continue

#             prices[sectorName] = price
#             break

#     try:
#         updatedEvent = service.update_event_prices_service(
#             organizerId,
#             eventId,
#             prices
#         )

#         print("\nPrecios actualizados correctamente.")

#         for sectorName, sectorData in updatedEvent["sectors"].items():
#             print(f"- {sectorName}: ${sectorData['price']}")

#     except ValueError as e:
#         print(f"\n[ERROR] {e}")

#     input("\nPresiona ENTER para volver al menú...")

# def view_sales_status(organizerId):
#     pass

#     print("\n" + "="*55)
#     print("       ESTADO DE VENTAS Y DISPONIBILIDAD".center(55))
#     print("="*55)

#     myEvents = service.get_events_by_organizer_service(organizerId)

#     if not myEvents:
#         print("\n[INFO] Todavía no tenés eventos publicados.")
#         input("\nPresiona ENTER para volver al menú...")
#         return

#     layout_helpers.events_board(myEvents)

#     eventId = input("\nIngrese el ID del evento que desea consultar: ").strip()

#     try:
#         stats = service.get_event_sales_status_service(
#             organizerId,
#             eventId
#         )

#         event = stats["event"]

#         print("\n" + "="*55)
#         print(f"EVENTO: {event['name']}")
#         print("="*55)

#         for sector in stats["sectors"]:
#             print(f"\nSector: {sector['name']}")
#             print(f"Capacidad: {sector['capacity']}")
#             print(f"Vendidos: {sector['sold']}")
#             print(f"Disponibles: {sector['available']}")
#             print(f"Ocupación: {sector['occupancy']:.1f}%")

#         print("\n" + "-"*55)
#         print("RESUMEN TOTAL")
#         print(f"Capacidad total: {stats['totalCapacity']}")
#         print(f"Entradas vendidas: {stats['totalSold']}")
#         print(f"Entradas disponibles: {stats['totalAvailable']}")
#         print(f"Ocupación total: {stats['totalOccupancy']:.1f}%")

#     except ValueError as e:
#         print(f"\n[ERROR] {e}")

#     input("\nPresiona ENTER para volver al menú...")
# def assign_category_to_event(organizerId):
#     pass
#     print("\n" + "="*55)
#     print("           ASIGNAR CATEGORÍA A UN EVENTO".center(55))
#     print("="*55)
    
#     myEvents = service.get_events_by_organizer_service(organizerId)
#     if not myEvents:
#         print("\n[INFO] No tenés ningún evento publicado para asignarle categorías.")
#         input("\nPresiona ENTER para volver al menú...")
#         return
        
#     layout_helpers.events_board(myEvents)
    
#     eventId = input("\nIngrese el ID (o los primeros caracteres) del evento: ").strip()
#     if not eventId:
#         print("\n[ADVERTENCIA] Operación cancelada.")
#         input("\nPresiona ENTER para volver...")
#         return
        
#     matching_events = [
#         e for e in myEvents 
#         if str(e.get("id")) == str(eventId) or str(e.get("id")).startswith(str(eventId))
#     ]
    
#     if not matching_events:
#         print("\n[ERROR] No se encontró ningún evento tuyo con ese ID.")
#         input("\nPresiona ENTER para volver...")
#         return
        
#     if len(matching_events) > 1:
#         print("\n[ERROR] Hay varios eventos que coinciden con ese prefijo de ID.")
#         print("Por favor, ingrese más caracteres del ID para identificarlo inequívocamente.")
#         input("\nPresiona ENTER para volver...")
#         return
        
#     target_event = matching_events[0]
    
#     print(f"\n[INFO] Evento seleccionado: '{target_event['name']}'")
#     if len(target_event.get("categories", [])) > 0:
#         print(f"Categoría actual: {target_event['categories'][0]}")
#     else:
#         print("Categoría actual: Ninguna")
    
#     availableCategories = ", ".join(categories)
#     print(f"\nCategorías disponibles: [{availableCategories}]")
#     new_cat = input("Ingrese la nueva categoría para el evento: ").strip()
    
#     try:
#         service.assign_category_service(
#             organizerId=organizerId,
#             eventId=target_event["id"],
#             category=new_cat
#         )
#         print("\n" + "-"*45)
#         print("¡Categoría asignada exitosamente!")
#         print("-" * 45)
#     except ValueError as e:
#         print(f"\n[ADVERTENCIA] {e}")
#     except Exception as e:
#         print(f"\n[ERROR CRÍTICO] Ocurrió un error inesperado: {e}")
        
#     input("\nPresiona ENTER para volver al menú principal...")
#     return
