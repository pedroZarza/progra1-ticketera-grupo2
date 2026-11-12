def selection_sort_by_name(items):
    ordered_items = items.copy()

    for i in range(len(ordered_items) - 1):
        min_position = i

        for j in range(i + 1, len(ordered_items)):
            if ordered_items[j]["name"].lower() < ordered_items[min_position]["name"].lower():
                min_position = j

        aux = ordered_items[i]
        ordered_items[i] = ordered_items[min_position]
        ordered_items[min_position] = aux

    return ordered_items

def bubble_sort_by_id(items):
    ordered_items = items.copy()

    for i in range(len(ordered_items) - 1):
        for j in range(len(ordered_items) - 1 - i):
            if ordered_items[j]["id"] > ordered_items[j + 1]["id"]:
                aux = ordered_items[j]
                ordered_items[j] = ordered_items[j + 1]
                ordered_items[j + 1] = aux

    return ordered_items

def insertion_sort_by_datetime(items):
    ordered_items = items.copy()

    for i in range(1, len(ordered_items)):
        current_item = ordered_items[i]
        j = i - 1

        while j >= 0 and ordered_items[j]["datetime"] > current_item["datetime"]:
            ordered_items[j + 1] = ordered_items[j]
            j -= 1

        ordered_items[j + 1] = current_item

    return ordered_items