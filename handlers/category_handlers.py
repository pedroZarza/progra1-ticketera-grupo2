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