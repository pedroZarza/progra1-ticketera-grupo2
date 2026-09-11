from utils import input_helpers
from services import user_service as service

def login():
    attempts = 1
    while attempts <= 3:
        username = input_helpers.prompt_non_empty_field("\nIngrese su nombre de usuario: ")
        if username.lower() == "q": return
        password = input_helpers.prompt_non_empty_field("Ingrese su contraseña: ")
        if username.lower() == "q": return
        user = service.authenticate_user(username, password)
        if user != None:
            print(f"Sesión iniciada exitosamente! Usuario: {user["username"]}")
            return user
        print(f"Credenciales Incorrectas. Intentos restantes: { 3 - attempts}")
        attempts += 1
    print("No posee más intentos.")
    input("\nPresiona ENTER para volver al menú principal...")
    return
    
        
def register_user():
    pass

    