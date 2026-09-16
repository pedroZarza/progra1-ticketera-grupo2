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