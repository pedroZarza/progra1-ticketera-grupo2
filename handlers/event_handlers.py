from services import event_service as service
from utils import layout_helpers
from data.categories_data import categories 
from utils import input_helpers
from utils.messages import show_error, show_info, show_success
from datetime import datetime

def show_events():
    events = service.read_all_events()
    layout_helpers.events_board(events)
    input("\nPresiona ENTER para volver al menú principal...")
    return

def show_event_detail():
    events = service.read_active_events()
    layout_helpers.events_board(events)
    eventId = input_helpers.prompt_non_empty_field(
        "\nIngrese el ID del evento que desea ver: "
    )

    if eventId.lower() == "q":
        return

    event = service.get_event_by_id(eventId)
    if event is None:
        show_error("No existe un evento con ese ID.")
        return

    eventDatetime = datetime.fromisoformat(event["datetime"])
    formattedDatetime = eventDatetime.strftime("%d/%m/%Y %H:%M")

    print(f"\n[{str(event['id'])[:8]}] {event['name']}") 
    print("-"*40)
    print(f"Fecha y hora: {formattedDatetime}")
    print(f"Venue: {event['venue']}")
    print(f"Categorías: {', '.join(event['categories'])}")
    print(f"Organizador: {event['organizer']}")
    print(f"Descripción: {event['description']}")
    print("\nSectores:")
    for sector_name, sector in event["sectors"].items():
        print(f"- {sector_name}: ${sector['price']}")
    input("\nPresiona ENTER para volver al menú principal...")
    return
    


def create_event(organizerId):
   
    print("\n" + "="*45)
    print("           CREAR NUEVO EVENTO")
    print("="*45)
    
    name = input("Ingrese el nombre del evento: ").strip()
    description = input("Ingrese una breve descripción: ").strip()
    
    dateStr = input("Ingrese la fecha (DD/MM/AAAA): ").strip()
    timeStr = input("Ingrese la hora (HH:MM): ").strip()
    
    datetimeStr = f"{dateStr} {timeStr}"

    availableCategories = ", ".join(categories)
    category = input(f"Ingrese la categoría ({availableCategories}): ").strip()
   
    venueIdStr = input("Ingrese el ID del Venue (Ej: 1): ").strip()

    if not all([name, description, dateStr, timeStr, category, venueIdStr]):
        print("\n[ERROR] Todos los campos son obligatorios. Operación cancelada.")
        input("\nPresiona ENTER para volver al menú...")
        return

    try:
        
        newEvent = service.create_event_service(
            organizerId=organizerId,
            name=name,
            datetimeStr=datetimeStr,
            category=category,
            venueIdStr=venueIdStr,
            description=description
        )
        
        print("\n" + "-"*45)
        print("¡El evento fue creado correctamente!")
        print(f"-> ID del Evento: {newEvent['id']}")
        print(f"-> Nombre: {newEvent['name']}")
        print(f"-> Sectores cargados: {', '.join(newEvent['sectors'].keys())}")
        print("-" * 45)
        print("* Recordá definir los precios por sector para habilitar la venta.")
        
    except ValueError as e:
        print(f"\n[ADVERTENCIA] {e}")
        
    except Exception as e:
        print(f"\n[ERROR CRÍTICO] Ocurrió un error inesperado: {e}")

    input("\nPresiona ENTER para volver al menú principal...")
    return

def view_my_events(organizerId):
    
    print("\n" + "="*55)
    print("              MIS EVENTOS PUBLICADOS".center(55))
    print("="*55)
    
    myEvents = service.get_events_by_organizer_service(organizerId)
    
    if not myEvents:
        print("\n[INFO] Todavía no tenés ningún evento publicado.")
    else:
        layout_helpers.events_board(myEvents)
            
    input("\nPresiona ENTER para volver al menú principal...")
    return

def search_event_by_name(organizerId):
    
    print("\n" + "="*55)
    print("              BUSCAR EVENTO POR NOMBRE".center(55))
    print("="*55)
    
    search_term = input("Ingrese el nombre exacto del evento a buscar: ").strip()
    
    if not search_term:
        print("\n[ADVERTENCIA] No ingresaste ningún texto de búsqueda.")
        input("\nPresiona ENTER para volver al menú...")
        return
        
    results = service.search_organizer_events_by_name_service(search_term, organizerId)
    
    if not results:
        print(f"\n[INFO] No se encontró ningún evento que se llame exactamente '{search_term}'.")
    else:
        print(f"\n[INFO] Evento encontrado:")
        layout_helpers.events_board(results)
        
    input("\nPresiona ENTER para volver al menú principal...")
    return

def search_event_by_category(organizerId):
    
    print("\n" + "="*55)
    print("            BUSCAR EVENTO POR CATEGORÍA".center(55))
    print("="*55)
    
    availableCategories = ", ".join(categories)
    category_term = input(f"Ingrese la categoría a buscar ({availableCategories}): ").strip()
    
    if not category_term:
        print("\n[ADVERTENCIA] No ingresaste ninguna categoría.")
        input("\nPresiona ENTER para volver al menú...")
        return
        
    results = service.search_organizer_events_by_category_service(category_term, organizerId)
    
    if not results:
        print(f"\n[INFO] No tenés eventos registrados en la categoría '{category_term}'.")
    else:
        print(f"\n[INFO] Se encontraron {len(results)} evento(s) de {category_term.capitalize()}:")
        layout_helpers.events_board(results)
        
    input("\nPresiona ENTER para volver al menú principal...")
    return

def edit_event(organizerId):
    print("\n" + "="*55)
    print("                 MODIFICAR EVENTO".center(55))
    print("="*55)
    
    myEvents = service.get_events_by_organizer_service(organizerId)
    if not myEvents:
        print("\n[INFO] No tenés ningún evento publicado para modificar.")
        input("\nPresiona ENTER para volver al menú...")
        return
        
    layout_helpers.events_board(myEvents)
    
    eventId = input("\nIngrese el ID (o los primeros caracteres) del evento a modificar: ").strip()
    if not eventId:
        print("\n[ADVERTENCIA] Operación cancelada.")
        input("\nPresiona ENTER para volver...")
        return
        
    matching_events = [
        e for e in myEvents 
        if str(e.get("id")) == str(eventId) or str(e.get("id")).startswith(str(eventId))
    ]
    
    if not matching_events:
        print("\n[ERROR] No se encontró ningún evento tuyo con ese ID.")
        input("\nPresiona ENTER para volver...")
        return
        
    if len(matching_events) > 1:
        print("\n[ERROR] Hay varios eventos que coinciden con ese prefijo de ID.")
        print("Por favor, ingrese más caracteres del ID para identificarlo inequívocamente.")
        input("\nPresiona ENTER para volver...")
        return
        
    target_event = matching_events[0]
    
    print(f"\n[INFO] Modificando: '{target_event['name']}'")
    print("Deje el campo en blanco y presione ENTER si no desea modificarlo.\n")
    
    new_name = input(f"Nuevo nombre [{target_event['name']}]: ").strip()
    new_desc = input(f"Nueva descripción [{target_event.get('description', '')}]: ").strip()
    
    availableCategories = ", ".join(categories)
    current_cat = target_event.get('category', '')
    new_cat = input(f"Nueva categoría ({availableCategories}) [{current_cat}]: ").strip()
    
    try:
        service.update_event_service(
            organizerId=organizerId,
            eventId=target_event["id"],
            name=new_name if new_name else None,
            description=new_desc if new_desc else None,
            category=new_cat if new_cat else None
        )
        print("\n" + "-"*45)
        print("¡El evento fue modificado exitosamente!")
        print("-" * 45)
    except ValueError as e:
        print(f"\n[ADVERTENCIA] {e}")
    except Exception as e:
        print(f"\n[ERROR CRÍTICO] Ocurrió un error inesperado: {e}")
        
    input("\nPresiona ENTER para volver al menú principal...")
    return
def define_event_prices(organizerId):

    print("\n" + "="*55)
    print("            DEFINIR PRECIOS POR SECTOR".center(55))
    print("="*55)

    myEvents = service.get_events_by_organizer_service(organizerId)

    if not myEvents:
        print("\n[INFO] Todavía no tenés eventos publicados.")
        input("\nPresiona ENTER para volver al menú...")
        return

    layout_helpers.events_board(myEvents)

    eventId = input("\nIngrese el ID del evento: ").strip()

    event = service.get_organizer_event_by_id_service(organizerId, eventId)

    if event is None:
        print("\n[ERROR] El evento no existe o no pertenece a tu usuario.")
        input("\nPresiona ENTER para volver al menú...")
        return

    prices = {}

    for sectorName, sectorData in event["sectors"].items():

        currentPrice = sectorData["price"]

        print(f"\nSector: {sectorName}")

        if currentPrice is None:
            print("Precio actual: sin definir")
        else:
            print(f"Precio actual: ${currentPrice}")

        while True:
            priceStr = input("Ingrese el nuevo precio: ").strip()

            if not priceStr.isdigit():
                print("[ERROR] El precio debe ser un número entero.")
                continue

            price = int(priceStr)

            if price <= 0:
                print("[ERROR] El precio debe ser mayor a cero.")
                continue

            prices[sectorName] = price
            break

    try:
        updatedEvent = service.update_event_prices_service(
            organizerId,
            eventId,
            prices
        )

        print("\nPrecios actualizados correctamente.")

        for sectorName, sectorData in updatedEvent["sectors"].items():
            print(f"- {sectorName}: ${sectorData['price']}")

    except ValueError as e:
        print(f"\n[ERROR] {e}")

    input("\nPresiona ENTER para volver al menú...")

def view_sales_status(organizerId):

    print("\n" + "="*55)
    print("       ESTADO DE VENTAS Y DISPONIBILIDAD".center(55))
    print("="*55)

    myEvents = service.get_events_by_organizer_service(organizerId)

    if not myEvents:
        print("\n[INFO] Todavía no tenés eventos publicados.")
        input("\nPresiona ENTER para volver al menú...")
        return

    layout_helpers.events_board(myEvents)

    eventId = input("\nIngrese el ID del evento que desea consultar: ").strip()

    try:
        stats = service.get_event_sales_status_service(
            organizerId,
            eventId
        )

        event = stats["event"]

        print("\n" + "="*55)
        print(f"EVENTO: {event['name']}")
        print("="*55)

        for sector in stats["sectors"]:
            print(f"\nSector: {sector['name']}")
            print(f"Capacidad: {sector['capacity']}")
            print(f"Vendidos: {sector['sold']}")
            print(f"Disponibles: {sector['available']}")
            print(f"Ocupación: {sector['occupancy']:.1f}%")

        print("\n" + "-"*55)
        print("RESUMEN TOTAL")
        print(f"Capacidad total: {stats['totalCapacity']}")
        print(f"Entradas vendidas: {stats['totalSold']}")
        print(f"Entradas disponibles: {stats['totalAvailable']}")
        print(f"Ocupación total: {stats['totalOccupancy']:.1f}%")

    except ValueError as e:
        print(f"\n[ERROR] {e}")

    input("\nPresiona ENTER para volver al menú...")
def assign_category_to_event(organizerId):
    
    print("\n" + "="*55)
    print("           ASIGNAR CATEGORÍA A UN EVENTO".center(55))
    print("="*55)
    
    myEvents = service.get_events_by_organizer_service(organizerId)
    if not myEvents:
        print("\n[INFO] No tenés ningún evento publicado para asignarle categorías.")
        input("\nPresiona ENTER para volver al menú...")
        return
        
    layout_helpers.events_board(myEvents)
    
    eventId = input("\nIngrese el ID (o los primeros caracteres) del evento: ").strip()
    if not eventId:
        print("\n[ADVERTENCIA] Operación cancelada.")
        input("\nPresiona ENTER para volver...")
        return
        
    matching_events = [
        e for e in myEvents 
        if str(e.get("id")) == str(eventId) or str(e.get("id")).startswith(str(eventId))
    ]
    
    if not matching_events:
        print("\n[ERROR] No se encontró ningún evento tuyo con ese ID.")
        input("\nPresiona ENTER para volver...")
        return
        
    if len(matching_events) > 1:
        print("\n[ERROR] Hay varios eventos que coinciden con ese prefijo de ID.")
        print("Por favor, ingrese más caracteres del ID para identificarlo inequívocamente.")
        input("\nPresiona ENTER para volver...")
        return
        
    target_event = matching_events[0]
    
    print(f"\n[INFO] Evento seleccionado: '{target_event['name']}'")
    print(f"Categoría actual: {target_event.get('category', 'Ninguna')}")
    
    availableCategories = ", ".join(categories)
    print(f"\nCategorías disponibles: [{availableCategories}]")
    new_cat = input("Ingrese la nueva categoría para el evento: ").strip()
    
    try:
        service.assign_category_service(
            organizerId=organizerId,
            eventId=target_event["id"],
            category=new_cat
        )
        print("\n" + "-"*45)
        print("¡Categoría asignada exitosamente!")
        print("-" * 45)
    except ValueError as e:
        print(f"\n[ADVERTENCIA] {e}")
    except Exception as e:
        print(f"\n[ERROR CRÍTICO] Ocurrió un error inesperado: {e}")
        
    input("\nPresiona ENTER para volver al menú principal...")
    return
