from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def get_id(self):
        return self.id

# This should be a database lookup in a real application
users = []

def get_user_by_username(username):
    return next((user for user in users if user.username == username), None)
