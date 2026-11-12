from repositories import category_repository


def get_categories():
    """Devuelve el catálogo de categorías.

    Retorna:
        list: nombres de categoría.
    """
    return category_repository.load_categories()

def add_category(category):
    """Agrega una categoría si no existe.

    Parámetros:
        category (str): nombre de la categoría.

    Retorna:
        str: la categoría agregada.
    """
    categories = category_repository.load_categories()

    for existing_category in categories:
        if existing_category.lower() == category.lower():
            raise ValueError("La categoría ya existe.")

    categories.append(category)
    category_repository.save_categories(categories)
    return category


def remove_category(category):
    """Elimina una categoría por nombre.

    Parámetros:
        category (str): nombre de la categoría.

    Retorna:
        str: la categoría eliminada.
    """
    categories = category_repository.load_categories()
    for existing_category in categories:
        if existing_category.lower() == category.lower():
            categories.remove(existing_category)
            category_repository.save_categories(categories)
            return existing_category

    raise LookupError("La categoría no existe.")
