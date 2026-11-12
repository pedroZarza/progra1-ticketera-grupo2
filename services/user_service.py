from repositories import user_repository
from utils.password_helpers import hash_password, verify_password


def get_all_users():
    users = user_repository.load_users()
    return users    

def get_active_users():
    users = user_repository.load_users()
    activeUsers = []
    for user in users:
        if user["active"] == True:
            activeUsers.append(user)
    return activeUsers

def get_user_by_id(user_id): #verificar esta función. No deberia servir.
    users = user_repository.load_users()
    for user in users:
        if str(user["id"]) == str(user_id):
            return user
    return None

def authenticate_user(username, password):
    users = get_active_users()
    for user in users:
        if user["username"] == username and verify_password(password, user["password"]):
            return user
    raise ValueError("Credenciales inválidas")


def create_user(newUserData):
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
    users = get_all_users()
    for user in users:
        if user["id"] == userId:
            user["password"] = hash_password(newPassword)
            user_repository.save_users(users)
            return user
    raise LookupError(f"No existe un usuario con id '{userId}'")


