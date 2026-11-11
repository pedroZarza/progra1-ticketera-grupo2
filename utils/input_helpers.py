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
    value = ""
    isValid = False

    while not isValid:
        value = input(message).strip()

        if value.lower() == "q": 
            isValid = True
            value = "q"
        elif value.isdigit() and int(value) > 0:
            isValid = True
            value = int(value)
        else:
            show_error("Ingrese un número entero mayor que cero, o 'q' para cancelar.")
    return value



def prompt_time_slot(message):
    isValid = False
    while not isValid:
        timeSlot = input(message).strip()
        if timeSlot.lower() == "q":
            return "q"

        parts = timeSlot.split(":")

        if len(parts) == 2 and len(parts[0]) == 2 and len(parts[1]) == 2:
            if parts[0].isdigit() and parts[1].isdigit():
                hour = int(parts[0])
                minute = int(parts[1])

                if 0 <= hour <= 23 and 0 <= minute <= 59:
                    isValid = True
        if not isValid:
            show_error("Ingrese un horario válido (HH:MM).")
    return timeSlot