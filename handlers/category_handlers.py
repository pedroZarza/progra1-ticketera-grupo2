from utils import input_helpers
from services import category_service as service
from utils.messages import show_error, show_success, show_info


def show_categories():
    categories = service.get_categories()
    if len(categories) == 0:
        show_info("No hay categorías disponibles.")
        return
    print("\nCategorías disponibles:")
    for category in categories:
        print(f"- {category}")
    input("\nPresiona ENTER para volver al menú principal...")
    return
    
def create_category():
    operationSuccess = False
    while not operationSuccess:
        category = input_helpers.prompt_non_empty_field("\nIngrese el nombre de la categoría: ")
        if category.lower() == "q": return

        try:
            service.add_category(category)
            show_success(f"Categoría '{category}' registrada exitosamente.")
            operationSuccess = True
        except ValueError as error:
            show_error(f"{error}")
            response = input("\nPresiona ENTER para volver a intentar o q para cancelar la operación...")
            if response.strip().lower() == "q":
                return
    return
              
def delete_category():
    operationSuccess = False
    categories = service.get_categories()
    if len(categories) == 0:
        show_info("No hay categorías disponibles.")
        return
    print("\nCategorías disponibles:")
    for category in categories:
        print(f"- {category}")

    while not operationSuccess:
        category = input_helpers.prompt_non_empty_field("\nIngrese el nombre de la categoría a eliminar: ")
        if category.lower() == "q": return

        try:
            service.remove_category(category)
            show_success(f"Categoría '{category}' eliminada exitosamente.")
            operationSuccess = True
            
        except LookupError as error:
            show_error(f"{error}")
            response = input("\nPresiona ENTER para volver a intentar o q para cancelar la operación...")
            if response.strip().lower() == "q":
                return
    return