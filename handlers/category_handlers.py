from utils import input_helpers
from services import category_service as service
from utils.messages import show_error, show_success


def create_category():
    category = input_helpers.prompt_non_empty_field(
        "\nIngrese el nombre de la categoría: "
    )

    if category.lower() == "q":
        return

    success = service.add_category(category)

    if success:
        show_success(f"Categoría '{category}' registrada exitosamente.")
    else:
        show_error("La categoría ya existe.")

def delete_category():
    category = input_helpers.prompt_non_empty_field(
        "\nIngrese el nombre de la categoría a eliminar: "
    )

    if category.lower() == "q":
        return

    success = service.remove_category(category)

    if success:
        show_success(f"Categoría '{category}' eliminada exitosamente.")
    else:
        show_error("La categoría no existe.")