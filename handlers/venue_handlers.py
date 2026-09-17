from services import venue_service as service
from utils import input_helpers
from utils.messages import show_info, show_success, show_error



def show_venues():
    venues = service.get_venues()

    if len(venues) == 0:
        show_info("No hay venues registrados.")
        return

    print("\nVENUES DEL SISTEMA")

    for venue in venues:
        print(f"\nID: {venue['id']}")
        print(f"Nombre: {venue['name']}")
        print(f"Dirección: {venue['address']}")
        print(f"Estado: {'Activo' if venue['active'] else 'Inactivo'}")
        print("Sectores:")

        for sector_name in venue["sectors"]:
            print(f"- {sector_name}")



def create_sectors():
    sectors = {}

    amount = input_helpers.prompt_positive_number("Ingrese la cantidad de sectores: ")

    for i in range(amount):
        print(f"\nSector {i + 1}")

        while True:
            name = input_helpers.prompt_non_empty_field("Nombre del sector: ")

            if name not in sectors:
                break

            show_error("Ya existe un sector con ese nombre.")

        while True:
            print("1. General")
            print("2. Numerado")
            sector_type = input("Seleccione el tipo de sector: ")

            if sector_type == "1" or sector_type == "2":
                break

            show_error("Seleccione una opción válida.")

        if sector_type == "1":
            capacity = input_helpers.prompt_positive_number("Ingrese la capacidad: ")

            sectors[name] = {
                "type": "general",
                "capacity": capacity
            }

        else:
            rows = input_helpers.prompt_positive_number("Ingrese la cantidad de asientos por fila: ")
            columns = input_helpers.prompt_positive_number("Ingrese la cantidad de filas de asientos del sector: ")

            sectors[name] = {
                "type": "numbered",
                "rows": rows,
                "columns": columns
            }

    return sectors

def create_venue():
    name = input_helpers.prompt_non_empty_field("Nombre del venue: ")

    if name.lower() == "q":
        return

    address = input_helpers.prompt_non_empty_field("Dirección: ")

    if address.lower() == "q":
        return

    time_slots = []
    amount = input_helpers.prompt_positive_number("Cantidad de horarios: ")

    for i in range(amount):
        while True:
            time_slot = input_helpers.prompt_non_empty_field(
                f"Horario {i + 1} (HH:MM): "
            )

            if time_slot.lower() == "q":
                return

            parts = time_slot.split(":")

            if len(parts) == 2 and len(parts[0]) == 2 and len(parts[1]) == 2:
                if parts[0].isdigit() and parts[1].isdigit():
                    hour = int(parts[0])
                    minute = int(parts[1])

                    if 0 <= hour <= 23 and 0 <= minute <= 59 and time_slot not in time_slots:
                        time_slots.append(time_slot)
                        break

            show_error("Ingrese un horario válido y no repetido (HH:MM).")

    sectors = create_sectors()

    success = service.create_venue(name, address, time_slots, sectors)

    if success:
        show_success("Venue registrado exitosamente.")
    else:
        show_error("Ya existe un venue con ese nombre.")

def edit_venue():
    show_venues()
    venue_id = input_helpers.prompt_non_empty_field(
        "\nIngrese el ID del venue que desea editar: "
    )

    if venue_id.lower() == "q":
        return

    new_name = input_helpers.prompt_non_empty_field(
        "Ingrese el nuevo nombre: "
    )

    new_address = input_helpers.prompt_non_empty_field(
        "Ingrese la nueva dirección: "
    )

    success = service.edit_venue(venue_id, new_name, new_address)

    if success:
        show_success("Venue editado exitosamente.")
    else:
        show_error("No existe un venue con ese ID.")


def delete_venue():
    show_venues()

    venue_id = input_helpers.prompt_non_empty_field(
        "\nIngrese el ID del venue que desea eliminar: "
    )

    if venue_id.lower() == "q":
        return

    success = service.delete_venue(venue_id)

    if success:
        show_success("Venue eliminado exitosamente.")
    else:
        show_error("No existe un venue con ese ID.")

def deactivate_venue():
    show_venues()

    venue_id = input_helpers.prompt_non_empty_field(
        "\nIngrese el ID del venue que desea inactivar: "
    )

    if venue_id.lower() == "q":
        return

    success = service.deactivate_venue(venue_id)

    if success:
        show_success("Venue inactivado exitosamente.")
    else:
        show_error("No existe un venue con ese ID.")

def show_venue_statistics():
    show_venues()

    venue_id = input_helpers.prompt_non_empty_field(
        "\nIngrese el ID del venue: "
    )

    if venue_id.lower() == "q":
        return

    for venue in service.get_venues():
        if str(venue["id"]) == venue_id:
            average, finished, upcoming = service.get_venue_statistics(venue["name"])

            print(f"\nEstadísticas de {venue['name']}")
            print(f"Ocupación promedio: {average:.2f}%")
            print(f"Eventos finalizados: {finished}")
            print(f"Eventos próximos: {upcoming}")
            return

    show_error("No existe un venue con ese ID.")