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