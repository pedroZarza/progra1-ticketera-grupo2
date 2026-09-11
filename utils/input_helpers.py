
def prompt_non_empty_field(message):
    field = ""
    is_valid = False
    while not is_valid:
        if field == "q": is_valid = True
        field = input(message).strip()
        if len(field) == 0:
            print("Este campo no puede estar vacío.")
        else:
            is_valid = True
    return field

    
    
def prompt_username_field(message):
    field = "" 
    is_valid = False
    while not is_valid:
        field = input(message).strip()
        if len(field) == 0:
            print("Este campo no puede estar vacío.")
        elif len(field) < 4:
            print("Debe ingresar un nombre de usuario de al menos 4 caracteres.")
        elif len(field) > 15:
            print("El nombre de usuario no puede tener más de 15 caracteres.")
        else:
            is_valid = True
    return field
                   