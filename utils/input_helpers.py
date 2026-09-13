import re
from utils.messages import show_error


def prompt_non_empty_field(message):
    field = ""
    isValid = False
    while not isValid:
        field = input(message).strip()
        if field == "q": isValid = True
        elif len(field) == 0:
            show_error("Este campo no puede estar vacío.")
        else:
            isValid = True
    return field

    
    
def prompt_username_field(message):
    field = "" 
    isValid = False
    while not isValid:
        field = input(message).strip()
        if field == "q": isValid = True
        elif len(field) == 0:
            show_error("Este campo no puede estar vacío.")
        elif len(field) < 4:
            show_error("Debe ingresar un nombre de usuario de al menos 4 caracteres.")
        elif len(field) > 15:
            show_error("El nombre de usuario no puede tener más de 15 caracteres.")
        else:
            isValid = True
    return field
                   

def prompt_password_field(message):
    field = ""
    isValid = False
    pattern = r"^(?=.*[A-Z])(?=.*\d).{8,}$"
    while not isValid:
        field = input(message).strip()
        if field == "q": isValid = True
        elif re.match(pattern, field):
            isValid = True
        else:
            show_error("La contraseña debe tener al menos 8 caracteres, una mayúscula y un número.")
    return field