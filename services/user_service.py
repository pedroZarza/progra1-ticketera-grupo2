from data import users_data

def authenticate_user(username, password):
    for user in users_data.users:
        if user["username"] == username and user["password"] == password:
            return user
    return None

def create_user():
    pass