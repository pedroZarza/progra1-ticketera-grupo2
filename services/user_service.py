from repositories import user_repository
from utils.password_helpers import hash_password, verify_password

def authenticate_user(username, password):
    users = user_repository.load_users()
    for user in users:
        if user["username"] == username and verify_password(password, user["password"]):
            return user
    raise ValueError("Credenciales inválidas")



def create_user(newUserData):
    users = user_repository.load_users()
    if len(users) > 0:
        newUserData["id"] = users[-1]["id"] + 1
    else:
        newUserData["id"] = 1
    for user in users:
        if str(user["username"]).lower() == str(newUserData["username"]).lower():
            raise ValueError("El nombre de usuario ya está registrado.")
    
    newUserData["password"] = hash_password(newUserData["password"])
    users.append(newUserData)
    user_repository.save_users(users)
    return newUserData


def get_user_by_id(user_id): #verificar esta función. No deberia servir.
    users = user_repository.load_users()
    for user in users:
        if str(user["id"]) == str(user_id):
            return user
    return None