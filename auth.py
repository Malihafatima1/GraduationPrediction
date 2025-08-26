from database import get_user, insert_user, validate_user

def register_user(username, email, password):
    if get_user(username):
        return False
    insert_user(username, email, password)
    return True

def login_user(username, password):
    if username == "admin" and password == "admin123":
        return "admin"
    if validate_user(username, password):
        return "student"
    return None
