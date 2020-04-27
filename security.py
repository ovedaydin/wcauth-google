from models.user import UserModel


def authenticate(username, password):
    user = UserModel.find_by_phone_number(username)
    if user and user.password == password:  # user exists and pasword true
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
