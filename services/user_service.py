from repositories import user_repository
from utils.password_helpers import hash_password, verify_password


def get_all_users():
    """Devuelve todos los usuarios registrados.

    Retorna:
        list: usuarios registrados.
    """
    users = user_repository.load_users()
    return users    

def get_active_users():
    """Devuelve solo los usuarios activos.

    Retorna:
        list: usuarios con la cuenta activa.
    """
    users = user_repository.load_users()
    activeUsers = []
    for user in users:
        if user["active"] == True:
            activeUsers.append(user)
    return activeUsers

def get_user_by_id(user_id): #verificar esta función. No deberia servir.
    """Busca un usuario por ID. Devuelve None si no existe.

    Parámetros:
        user_id (int): identificador del usuario.

    Retorna:
        dict o None: el usuario encontrado, o None si no existe.
    """
    users = user_repository.load_users()
    for user in users:
        if str(user["id"]) == str(user_id):
            return user
    return None

def authenticate_user(username, password):
    """Valida usuario y contraseña de una cuenta activa.

    Parámetros:
        username (str): nombre de usuario.
        password (str): contraseña en texto plano.

    Retorna:
        dict: el usuario autenticado.
    """
    users = get_active_users()
    for user in users:
        if user["username"] == username and verify_password(password, user["password"]):
            return user
    raise ValueError("Credenciales inválidas")


def create_user(newUserData):
    """Registra un usuario nuevo con la contraseña hasheada.

    Parámetros:
        newUserData (dict): username, password y role.

    Retorna:
        dict: el usuario creado.
    """
    users = user_repository.load_users()
    if len(users) > 0:
        newId = users[-1]["id"] + 1
    else:
        newId = 1
    for user in users:
        if str(user["username"]).lower() == str(newUserData["username"]).lower():
            raise ValueError("El nombre de usuario ya está registrado.")

    user = {
        "id": newId,
        "username": newUserData["username"],
        "password": hash_password(newUserData["password"]),
        "role": newUserData["role"],
        "active": True,
    }
    users.append(user)
    user_repository.save_users(users)
    return user


def deactivate_user(userId):
    """Marca un usuario como inactivo. No permite inactivar admins.

    Parámetros:
        userId (int): identificador del usuario.

    Retorna:
        dict: el usuario inactivado.
    """
    users = get_all_users()
    for user in users:
        if user["id"] == userId:
            if user["role"] == "admin":
                raise ValueError("No se puede inactivar un usuario administrador.")
            if user["active"] == False:
                raise ValueError("El usuario ya se encuentra inactivo.")
            user["active"] = False
            user_repository.save_users(users)
            return user
    raise LookupError(f"No existe un usuario con id '{userId}'")


def activate_user(userId):
    """Marca un usuario inactivo como activo.

    Parámetros:
        userId (int): identificador del usuario.

    Retorna:
        dict: el usuario activado.
    """
    users = get_all_users()
    for user in users:
        if user["id"] == userId:
            if user["active"] == True:
                raise ValueError("El usuario ya se encuentra activo.")
            user["active"] = True
            user_repository.save_users(users)
            return user
    raise LookupError(f"No existe un usuario con id '{userId}'")


def update_password(userId, newPassword):
    """Reemplaza la contraseña de un usuario.

    Parámetros:
        userId (int): identificador del usuario.
        newPassword (str): nueva contraseña en texto plano.

    Retorna:
        dict: el usuario actualizado.
    """
    users = get_all_users()
    for user in users:
        if user["id"] == userId:
            user["password"] = hash_password(newPassword)
            user_repository.save_users(users)
            return user
    raise LookupError(f"No existe un usuario con id '{userId}'")


