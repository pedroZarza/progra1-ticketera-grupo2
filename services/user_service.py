from data import users_data

def authenticate_user(username, password):
    for user in users_data.users:
        if user["username"] == username and user["password"] == password:
            return True, user
    return False, "invalid_credentials"

def create_user(newUserData):
    if len(users_data.users) > 0:
        newUserData["id"] = users_data.users[-1]["id"] + 1
    else:
        newUserData["id"] = 1
        
    for user in users_data.users:
        if str(user["username"]).lower() == str(newUserData["username"]).lower():
            return False, "username_taken" 
    users_data.users.append(newUserData)
    print(users_data.users)
    return True, newUserData