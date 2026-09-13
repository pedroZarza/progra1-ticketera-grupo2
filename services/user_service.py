from data import users_data

def authenticate_user(username, password):
    for user in users_data.users:
        if user["username"] == username and user["password"] == password:
            return True, user
    return False, "invalid_credentials"

def create_user(newUserData):
    for user in users_data.users:
        if str(user["username"]).lower() == str(newUserData["username"]).lower():
            return False, "username_taken" 
    users_data.users.append(newUserData)
    return True, newUserData