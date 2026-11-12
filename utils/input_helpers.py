import re
from datetime import datetime
from utils.messages import show_error


def prompt_non_empty_field(message):
    """Pide un texto no vacío. 'q' cancela.

    Parámetros:
        message (str): texto del pedido.

    Retorna:
        str: el texto ingresado, o 'q' si cancela.
    """
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
    """Pide si la cuenta es de organizador o de comprador.

    Retorna:
        str: 'organizer', 'customer' o 'q' si cancela.
    """
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
    """Pide un usuario de 4 a 15 caracteres, sin símbolos especiales.

    Parámetros:
        message (str): texto del pedido.

    Retorna:
        str: el usuario ingresado, o 'q' si cancela.
    """
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
    """Pide una contraseña de al menos 8 caracteres, con mayúscula y número.

    Parámetros:
        message (str): texto del pedido.

    Retorna:
        str: la contraseña ingresada, o 'q' si cancela.
    """
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
    """Pide un entero mayor a cero. 'q' cancela.

    Parámetros:
        message (str): texto del pedido.

    Retorna:
        int o str: el número, o 'q' si cancela.
    """
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
    """Pide un horario en formato HH:MM.

    Parámetros:
        message (str): texto del pedido.

    Retorna:
        str: el horario, o 'q' si cancela.
    """
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


def prompt_list_option(message, options):
    """Pide una opción de la lista, por número o por texto.

    Parámetros:
        message (str): texto del pedido.
        options (list): opciones válidas.

    Retorna:
        str: la opción elegida, o 'q' si cancela.
    """
    isValid = False
    while not isValid:
        value = input(message).strip()
        if value.lower() == "q":
            return "q"

        if value.isdigit():
            index = int(value)
            if 1 <= index <= len(options):
                return options[index - 1]

        for option in options:
            if option.lower() == value.lower():
                return option

        show_error("Seleccione una opción de la lista.")


def prompt_date(message):
    """Pide una fecha futura en formato DD/MM/AAAA.

    Parámetros:
        message (str): texto del pedido.

    Retorna:
        str: la fecha, o 'q' si cancela.
    """
    isValid = False
    while not isValid:
        date = input(message).strip()
        if date.lower() == "q":
            return "q"

        parsedDate = None
        parts = date.split("/")
        if len(parts) == 3 and len(parts[0]) == 2 and len(parts[1]) == 2 and len(parts[2]) == 4:
            if parts[0].isdigit() and parts[1].isdigit() and parts[2].isdigit():
                try:
                    parsedDate = datetime(int(parts[2]), int(parts[1]), int(parts[0]))
                except ValueError:
                    parsedDate = None

        if parsedDate is None:
            show_error("Ingrese una fecha válida (DD/MM/AAAA).")
        elif parsedDate.date() < datetime.now().date():
            show_error("La fecha del evento no puede ser en el pasado.")
        else:
            isValid = True
    return date



def prompt_price(message):
    """Pide un precio mayor a cero.

    Parámetros:
        message (str): texto del pedido.

    Retorna:
        float o str: el precio redondeado, o 'q' si cancela.
    """
    isValid = False
    while not isValid:
        value = input(message).strip()

        if value.lower() == "q":
            return "q"

        try:
            price = float(value)

            if price > 0:
                isValid = True
            else:
                show_error("El precio debe ser mayor a cero.")

        except ValueError:
            show_error("Ingrese un precio válido.")

    return round(price, 2)