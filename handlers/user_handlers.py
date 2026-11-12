from utils import input_helpers
from services import user_service as service
from utils.messages import show_error, show_success, show_info, show_warning

def login():
    attempts = 1
    while attempts <= 3:
        username = input_helpers.prompt_non_empty_field("\nIngrese su nombre de usuario: ")
        if username.lower() == "q": return
        password = input_helpers.prompt_non_empty_field("Ingrese su contraseña: ")
        if password.lower() == "q": return
        try:
            user = service.authenticate_user(username, password)
            show_success(f"Sesión iniciada exitosamente! Usuario: {user['username']}")
            return user
        except ValueError as error:
            show_error(f"{error}. Intentos restantes: { 3 - attempts}")
            attempts += 1
    show_info("No posee más intentos.")
    input("\nPresiona ENTER para volver al menú principal...")
    return
    
def register_user():
    operationSuccess = False
    user = None
    while not operationSuccess:
        role = input_helpers.prompt_role_selection()
        if role.lower() == "q": return
        username = input_helpers.prompt_username_field("\nIngrese un nombre de usuario (min. 4 caracteres): ")
        if username.lower() == "q": return
        password = input_helpers.prompt_password_field("Ingrese una contraseña: ")
        if password.lower() == "q": return
        passwordCheck = input("Ingrese nuevamente la contraseña: ")
        if passwordCheck.lower() == "q": return
        while password != passwordCheck:
            show_error("Las contraseñas no coinciden")
            passwordCheck = input("Ingrese nuevamente la contraseña: ")
            if passwordCheck.lower() == "q": return
        newUser = {  
            "username": username, 
            "password": password, 
            "role": role
        }
        try: 
            user = service.create_user(newUser)
            show_success(f'Usuario {user["username"]} registrado exitosamente!')
            operationSuccess = True
        except ValueError as error:
            show_error(f"{error}")
            response = input("\nPresiona ENTER para volver a intentar o q para cancelar la operación...")
            if response.strip().lower() == "q": return
    return user


def deactivate_user():
    users = service.get_all_users()
    if len(users) == 0:
        show_info("No hay usuarios registrados.")
        input("\nPresiona ENTER para volver al menú principal...")
        return

    print("\nUSUARIOS")
    for user in users:
        status = "Activo" if user["active"] else "Inactivo"
        print(f"[{user['id']}] {user['username']} | {status}")

    operationSuccess = False
    while not operationSuccess:
        userId = input_helpers.prompt_positive_number("\nIngrese el ID del usuario que desea inactivar: ")
        if userId == "q":
            return
        try:
            user = service.deactivate_user(userId)
            show_success(f"El usuario '{user['username']}' fue inactivado correctamente.")
            operationSuccess = True
        except (ValueError, LookupError) as error:
            show_error(error)
            response = input("\nPresiona ENTER para volver a intentar o q para cancelar la operación...")
            if response.strip().lower() == "q":
                return
    input("\nPresiona ENTER para volver al menú principal...")


def activate_user():
    users = service.get_all_users()
    if len(users) == 0:
        show_info("No hay usuarios registrados.")
        input("\nPresiona ENTER para volver al menú principal...")
        return

    print("\nUSUARIOS")
    for user in users:
        status = "Activo" if user["active"] else "Inactivo"
        print(f"[{user['id']}] {user['username']} | {status}")

    operationSuccess = False
    while not operationSuccess:
        userId = input_helpers.prompt_positive_number("\nIngrese el ID del usuario que desea activar: ")
        if userId == "q":
            return
        try:
            user = service.activate_user(userId)
            show_success(f"El usuario '{user['username']}' fue activado correctamente.")
            operationSuccess = True
        except (ValueError, LookupError) as error:
            show_error(error)
            response = input("\nPresiona ENTER para volver a intentar o q para cancelar la operación...")
            if response.strip().lower() == "q":
                return
    input("\nPresiona ENTER para volver al menú principal...")


def reset_password():
    users = service.get_all_users()
    if len(users) == 0:
        show_info("No hay usuarios registrados.")
        input("\nPresiona ENTER para volver al menú principal...")
        return

    print("\nUSUARIOS")
    for user in users:
        status = "Activo" if user["active"] else "Inactivo"
        print(f"[{user['id']}] {user['username']} | {status}")

    operationSuccess = False
    while not operationSuccess:
        userId = input_helpers.prompt_positive_number("\nIngrese el ID del usuario: ")
        if userId == "q":
            return

        password = input_helpers.prompt_password_field("\nIngrese la nueva contraseña: ")
        if password.lower() == "q":
            return
        passwordCheck = input("Ingrese nuevamente la contraseña: ")
        if passwordCheck.lower() == "q":
            return
        while password != passwordCheck:
            show_error("Las contraseñas no coinciden.")
            passwordCheck = input("Ingrese nuevamente la contraseña: ")
            if passwordCheck.lower() == "q":
                return
        try:
            user = service.update_password(userId, password)
            show_success(f"La contraseña del usuario '{user['username']}' fue restablecida.")
            operationSuccess = True
        except LookupError as error:
            show_error(error)
            response = input("\nPresiona ENTER para volver a intentar o q para cancelar la operación...")
            if response.strip().lower() == "q":
                return
    input("\nPresiona ENTER para volver al menú principal...")