import uuid  # <-- NUEVA IMPORTACIÓN
from utils import input_helpers
from services import user_service as service
from utils.messages import show_error, show_success, show_info, show_warning

def login():
    attempts = 1
    while attempts <= 3:
        username = input_helpers.prompt_non_empty_field("\nIngrese su nombre de usuario: ")
        if username.lower() == "q": return
        password = input_helpers.prompt_non_empty_field("Ingrese su contraseña: ")
        if username.lower() == "q": return
        success, user = service.authenticate_user(username, password)
        if success:
            show_success(f"Sesión iniciada exitosamente! Usuario: {user['username']}")
            return user
        show_error(f"Credenciales Incorrectas. Intentos restantes: { 3 - attempts}")
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
            "id": str(uuid.uuid4()), 
            "username": username, 
            "password": password, 
            "role": role
        }
        
        success, user = service.create_user(newUser)
        if success:
            show_success(f'Usuario {user["username"]} registrado exitosamente!')
            operationSuccess = True
        else:
            show_error("El nombre de usuario ya está registrado. Inicie sesión con su cuenta.")
            response = input("\nPresiona ENTER para volver a intentar o q para cancelar la operación...")
            if response == "q": return
    return user