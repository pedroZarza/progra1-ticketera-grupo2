from data import categories_data


def add_category(category):
    for existing_category in categories_data.categories:
        if existing_category.lower() == category.lower():
            return False

    categories_data.categories.append(category)
    return True

def remove_category(category):
    for existing_category in categories_data.categories:
        if existing_category.lower() == category.lower():
            categories_data.categories.remove(existing_category)
            return True

    return False

def get_categories():
    return categories_data.categories