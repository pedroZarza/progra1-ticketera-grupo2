from services import venue_service 
from utils import input_helpers
from utils.messages import show_info, show_success, show_error
from utils import layout_helpers



def show_venues():
    venues = venue_service.get_all_venues()
    if len(venues) == 0:
        show_info("No hay venues registrados.")
        return
    layout_helpers.venues_board(venues)
    input("\nPresiona ENTER para volver al menú principal...")
    return

def show_venue_detail():
    operationSuccess = False
    venues = venue_service.get_all_venues()
    if len(venues) == 0:
        show_info("No hay venues disponibles.")
        return

    layout_helpers.venues_board(venues)

    while not operationSuccess:
        venueId = input_helpers.prompt_positive_number(
            "\nIngrese el ID del venue que desea ver: "
        )
        if venueId == "q":
            return
        try:
            venue = venue_service.get_venue_by_id(venueId)
            layout_helpers.venue_detail(venue)
            operationSuccess = True
        except LookupError as error:
            show_error(error)
            response = input(
                "\nPresiona ENTER para volver a intentar o q para cancelar la operación..."
            )
            if response.strip().lower() == "q":
                return
    input("\nPresiona ENTER para volver al menú principal...")



def create_venue():
    print("\n- REGISTRAR NUEVO VENUE -")
    operationSuccess = False
    while not operationSuccess:
        name = input_helpers.prompt_non_empty_field("\nNombre del venue: ")
        if name.lower() == "q": return

        address = input_helpers.prompt_non_empty_field("Dirección: ")
        if address.lower() == "q": return

        quantity = input_helpers.prompt_positive_number("Cantidad de horarios: ")
        if quantity == "q": return

        timeSlots = []

        for i in range(quantity):
            isValid = False

            while not isValid:
                timeSlot = input_helpers.prompt_time_slot(f"\nHorario {i + 1} (HH:MM): ")

                if timeSlot.lower() == "q":
                    return
                elif timeSlot in timeSlots:
                    show_error("El horario ingresado ya existe.")
                else:
                    timeSlots.append(timeSlot)
                    isValid = True
        sectors = create_sectors()
        if sectors is None: return
        try:
            venue = venue_service.create_venue(name, address, timeSlots, sectors)
            show_success("El venue ha sido dado de alta con éxito.")
            print(f"\n[{venue['id']}] {venue['name']}")
            operationSuccess = True
        except ValueError as error:
            show_error(error)
            response = input("\nPresiona ENTER para volver a intentar o q para cancelar la operación...")
            if response.strip().lower() == "q":
                return
    input("\nPresiona ENTER para volver al menú principal...")


def create_sectors():
    sectors = {}
    quantity = input_helpers.prompt_positive_number("\nIngrese la cantidad de sectores: ")
    if quantity == "q": return
    for i in range(quantity):
        print(f"\nSector {i + 1}")

        while True:
            name = input_helpers.prompt_non_empty_field("Nombre del sector: ")
            if name.lower() == "q": return

            if name not in sectors:
                break

            show_error("Ya existe un sector con ese nombre.")

        while True:
            print("1. General")
            print("2. Numerado")
            sectorType = input("Seleccione el tipo de sector: ").strip()

            if sectorType.lower() == "q": return

            if sectorType == "1" or sectorType == "2":
                break

            show_error("Seleccione una opción válida.")

        if sectorType == "1":
            capacity = input_helpers.prompt_positive_number("Ingrese la capacidad: ")
            if capacity == "q": return

            sectors[name] = {
                "type": "general",
                "capacity": capacity
            }
        else:
            rows = input_helpers.prompt_positive_number("Ingrese la cantidad de filas de asientos del sector: ")
            if rows == "q": return

            columns = input_helpers.prompt_positive_number("Ingrese la cantidad de asientos por fila: ")
            if columns == "q": return

            sectors[name] = {
                "type": "numbered",
                "rows": rows,
                "columns": columns
            }
    return sectors



def edit_venue_info():
    operationSuccess = False
    venues = venue_service.get_all_venues()
    if len(venues) == 0:
        show_info("No hay venues disponibles.")
        return

    layout_helpers.venues_board(venues)

    while not operationSuccess:
        venueId = input_helpers.prompt_positive_number("\nIngrese el ID del venue que desea editar: ")
        if venueId == "q": return

        newName = input_helpers.prompt_non_empty_field("Ingrese el nuevo nombre: ")
        if newName.lower() == "q": return

        newAddress = input_helpers.prompt_non_empty_field("Ingrese la nueva dirección: ")
        if newAddress.lower() == "q": return
        try:
            venue_service.update_venue_by_id(venueId, newName, newAddress)
            show_success("Venue editado exitosamente.")
            operationSuccess = True
        except (ValueError, LookupError) as error:
            show_error(error)
            response = input("\nPresiona ENTER para volver a intentar o q para cancelar la operación...")
            if response.strip().lower() == "q": return
    input("\nPresiona ENTER para volver al menú principal...")



def edit_venue_time_slots():
    operationSuccess = False
    venues = venue_service.get_all_venues()

    if len(venues) == 0:
        show_info("No hay venues disponibles.")
        return

    layout_helpers.venues_board(venues)

    while True:
        venueId = input_helpers.prompt_positive_number("\nIngrese el ID del venue del cual desea editar horarios: ")
        if venueId == "q": return

        try:
            venue = venue_service.get_venue_by_id(venueId)
            break
        except LookupError as error:
            show_error(error)
            response = input("\nPresiona ENTER para volver a intentar o q para cancelar la operación...")
            if response.strip().lower() == "q": return

    print(f"\n{venue['name']} - Horarios actuales:")
    for slot in venue["time_slots"]:
        print(f"- {slot}")

    while True:
        print("\n1. Agregar nuevo horario")
        print("2. Eliminar horario existente")
        option = input("\nSeleccione una opción (q para cancelar): ").strip()

        if option.lower() == "q": return

        if option == "1" or option == "2":
            break

        show_error("Seleccione una opción válida.")

    while not operationSuccess:
        timeSlot = input_helpers.prompt_time_slot("\nIngrese el horario (HH:MM): ")
        if timeSlot.lower() == "q": return

        try:
            match option:
                case "1":
                    venue_service.add_venue_time_slot(venueId, timeSlot)
                    show_success("El nuevo horario fue agregado con éxito.")

                case "2":
                    venue_service.remove_venue_time_slot(venueId, timeSlot)
                    show_success("El horario fue eliminado correctamente.")

            operationSuccess = True

        except (ValueError, LookupError) as error:
            show_error(error)
            response = input("\nPresiona ENTER para volver a intentar o q para cancelar la operación...")
            if response.strip().lower() == "q": return

    input("\nPresiona ENTER para volver al menú principal...")
            
            
            
def edit_venue_sectors():
    venues = venue_service.get_all_venues()
    if len(venues) == 0:
        show_info("No hay venues disponibles.")
        return
    layout_helpers.venues_board(venues)
    while True:
        venueId = input_helpers.prompt_positive_number(
            "\nIngrese el ID del venue que desea modificar: "
        )
        if venueId == "q": return

        try:
            venue = venue_service.get_venue_by_id(venueId)
            break

        except LookupError as error:
            show_error(error)
    while True:
        layout_helpers.venue_detail(venue)
        print("Menú de edición de sectores:")
        print("\n1. Agregar sector")
        print("2. Eliminar sector")
        print("3. Modificar sector")
        option = input("\nSeleccione una opción (q para cancelar): ").strip().lower()
        if option == "q":
            return
        match option:
            case "1":
                add_venue_sector(venue)

            case "2":
                remove_venue_sector(venue)

            case "3":
                update_venue_sector(venue)

            case _:
                show_error("Seleccione una opción válida.")

        venue = venue_service.get_venue_by_id(venueId)



def add_venue_sector(venue):
    operationSuccess = False

    while not operationSuccess:
        sectorName = input_helpers.prompt_non_empty_field(
            "\nIngrese el nombre del nuevo sector: "
        )
        if sectorName.lower() == "q": return

        if sectorName.lower() in [name.lower() for name in venue["sectors"]]:
            show_error("Ya existe un sector con ese nombre.")
            continue

        while True:
            print("\n1. General")
            print("2. Numerado")

            sectorType = input("Seleccione el tipo de sector: ").strip().lower()
            if sectorType == "q": return

            if sectorType == "1" or sectorType == "2":
                break

            show_error("Seleccione una opción válida.")

        if sectorType == "1":
            capacity = input_helpers.prompt_positive_number(
                "Ingrese la capacidad: "
            )
            if capacity == "q": return

            sectorData = {
                "type": "general",
                "capacity": capacity
            }

        else:
            rows = input_helpers.prompt_positive_number(
                "Ingrese la cantidad de filas: "
            )
            if rows == "q": return

            columns = input_helpers.prompt_positive_number(
                "Ingrese la cantidad de asientos por fila: "
            )
            if columns == "q": return

            sectorData = {
                "type": "numbered",
                "rows": rows,
                "columns": columns
            }

        try:
            venue_service.add_venue_sector(
                venue["id"], sectorName, sectorData
            )

            show_success(f"El sector '{sectorName}' fue agregado correctamente.")
            operationSuccess = True

        except (ValueError, LookupError) as error:
            show_error(error)
    input("\nPresiona ENTER para volver al menú principal...")

def remove_venue_sector(venue):
    operationSuccess = False

    while not operationSuccess:
        sectorName = input_helpers.prompt_non_empty_field(
            "\nIngrese el nombre del sector que desea eliminar: "
        )
        if sectorName.lower() == "q": return

        try:
            venue_service.remove_venue_sector(venue["id"], sectorName)

            show_success(f"El sector '{sectorName}' fue eliminado correctamente.")
            operationSuccess = True

        except (ValueError, LookupError) as error:
            show_error(error)
    input("\nPresiona ENTER para volver al menú principal...")
    

def update_venue_sector(venue):
    operationSuccess = False
    while not operationSuccess:
        sectorName = input_helpers.prompt_non_empty_field(
            "\nIngrese el nombre del sector que desea modificar: "
        )
        if sectorName.lower() == "q": return

        if sectorName not in venue["sectors"]:
            show_error("El sector ingresado no existe en el venue.")
            continue

        sector = venue["sectors"][sectorName]

        if sector["type"] == "general":
            print(f"\nCapacidad actual: {sector['capacity']}")

            capacity = input_helpers.prompt_positive_number(
                "Ingrese la nueva capacidad: "
            )
            if capacity == "q": return

            sectorData = {
                "capacity": capacity
            }

        elif sector["type"] == "numbered":
            print(
                f"\nConfiguración actual: "
                f"{sector['rows']} filas x {sector['columns']} columnas"
            )

            rows = input_helpers.prompt_positive_number(
                "Ingrese la nueva cantidad de filas: "
            )
            if rows == "q": return

            columns = input_helpers.prompt_positive_number(
                "Ingrese la nueva cantidad de asientos por fila: "
            )
            if columns == "q": return

            sectorData = {
                "rows": rows,
                "columns": columns
            }

        try:
            venue_service.update_venue_sector(
                venue["id"], sectorName, sectorData
            )

            show_success(f"El sector '{sectorName}' fue actualizado correctamente.")
            operationSuccess = True

        except (ValueError, LookupError) as error:
            show_error(error)
    input("\nPresiona ENTER para volver al menú principal...")
   
   
   
         
def deactivate_venue():
    operationSuccess = False
    venues = venue_service.get_active_venues()
    if len(venues) == 0:
        show_info("No hay venues disponibles.")
        return

    layout_helpers.venues_board(venues)

    while not operationSuccess:
        venueId = input_helpers.prompt_positive_number("\nIngrese el ID del venue que desea inactivar: ")
        if venueId == "q": return

        try:
            venue = venue_service.deactivate_venue(venueId)
            show_success(f"El venue '{venue['name']}' fue inactivado correctamente.")
            operationSuccess = True
        except (ValueError, LookupError) as error:
            show_error(error)
            response = input("\nPresiona ENTER para volver a intentar o q para cancelar la operación...")
            if response.strip().lower() == "q": return
    input("\nPresiona ENTER para volver al menú principal...")


def activate_venue():
    operationSuccess = False
    venues = venue_service.get_deactive_venues()
    if len(venues) == 0:
        show_info("No hay venues disponibles.")
        return
    layout_helpers.venues_board(venues)
    while not operationSuccess:
        venueId = input_helpers.prompt_positive_number("\nIngrese el ID del venue que desea activar: ")     
        if venueId == "q": return
        try:
            venue = venue_service.activate_venue(venueId)
            show_success(f"El venue '{venue['name']}' fue activado correctamente.")
            operationSuccess = True
        except (ValueError, LookupError) as error:
            show_error(error)
            response = input("\nPresiona ENTER para volver a intentar o q para cancelar la operación...")
            if response.strip().lower() == "q": return
    input("\nPresiona ENTER para volver al menú principal...")



def delete_venue():
    operationSuccess = False
    venues = venue_service.get_all_venues()
    if len(venues) == 0:
        show_info("No hay venues disponibles.")
        return

    layout_helpers.venues_board(venues)

    while not operationSuccess:
        venueId = input_helpers.prompt_positive_number("\nIngrese el ID del venue que desea eliminar: ")
        if venueId == "q": return

        try:
            venue = venue_service.delete_venue(venueId)
            show_success(f"El venue '{venue['name']}' fue eliminado correctamente.")
            operationSuccess = True
        except (ValueError, LookupError) as error:
            show_error(error)
            response = input("\nPresiona ENTER para volver a intentar o q para cancelar la operación...")
            if response.strip().lower() == "q": return
    input("\nPresiona ENTER para volver al menú principal...")




# def show_venue_statistics():
#     show_venues()

#     venue_id = input_helpers.prompt_non_empty_field(
#         "\nIngrese el ID del venue: "
#     )

#     if venue_id.lower() == "q":
#         return

#     for venue in venue_service.get_venues():
#         if str(venue["id"]) == venue_id:
#             average, finished, upcoming = venue_service.get_venue_statistics(venue["name"])

#             print(f"\nEstadísticas de {venue['name']}")
#             print(f"Ocupación promedio: {average:.2f}%")
#             print(f"Eventos finalizados: {finished}")
#             print(f"Eventos próximos: {upcoming}")
#             return

#     show_error("No existe un venue con ese ID.")