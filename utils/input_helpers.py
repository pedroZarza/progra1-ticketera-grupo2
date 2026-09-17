import re
from utils.messages import show_error


def prompt_non_empty_field(message):
    field = ""
    isValid = False
    while not isValid:
        field = input(message).strip()
        if field.lower() == "q": isValid = True
        elif len(field) == 0:
            show_error("Este campo no puede estar vacío.")
        else:
            isValid = True
    return field

def prompt_role_selection():
    field = ""
    isValid = False
    while not isValid:
        print("\n¿Qué tipo de cuenta quieres crear?")
        print("1. Organizador")
        print("2. Comprador")
        option = input("\n>>> ").strip()
        match option:
            case "q":
                field = "q"
                isValid = True
            case "Q":
                field = "Q"
                isValid = True
            case "1":
                field = "organizer"
                isValid = True
            case "2":
                field = "customer"
                isValid = True
            case _:
                show_error("Opción inválida, elija una opción existente.")
    return field
    
def prompt_username_field(message):
    field = "" 
    isValid = False
    pattern = r"^[A-Za-zÑñ0-9_-]+$"
    while not isValid:
        field = input(message).strip()
        if field.lower() == "q": isValid = True
        elif len(field) == 0:
            show_error("Este campo no puede estar vacío.")
        elif len(field) < 4:
            show_error("Debe ingresar un nombre de usuario de al menos 4 caracteres.")
        elif len(field) > 15:
            show_error("El nombre de usuario no puede tener más de 15 caracteres.")
        elif not re.match(pattern, field):
            show_error("No se permiten caracteres especiales. El nombre de usuario solo puede contener letras, números, '_' y '-'.")
        else:
            isValid = True
    return field
                   

def prompt_password_field(message):
    field = ""
    isValid = False
    pattern = r"^(?=.*[A-Z])(?=.*\d).{8,}$"
    while not isValid:
        field = input(message).strip()
        if field.lower() == "q": isValid = True
        elif re.match(pattern, field):
            isValid = True
        else:
            show_error("La contraseña debe tener al menos 8 caracteres, una mayúscula y un número.")
    return field


def prompt_positive_number(message):
    while True:
        value = input(message).strip()

        if value.isdigit() and int(value) > 0:
            return int(value)

        show_error("Ingrese un número entero mayor que cero.")