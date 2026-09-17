from services import event_service as service
from utils import layout_helpers
from data.categories_data import categories 

def show_events():
    events = service.read_all_events()
    layout_helpers.events_board(events)
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
        print(f"-> Sectores cargados: {', '.join(newEvent['sectorPrices'].keys())}")
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