# dummy data blm setting database
users = [
    {'username': 'user1', 'password': 'password1', 'negara_asal': 'Indonesia'},
    {'username': 'user2', 'password': 'password2', 'negara_asal': 'Malaysia'},
]

def login(username, password):
    for user in users:
        if user['username'] == username and user['password'] == password:
            return [user]
    return []

def register(username, password, negara_asal):
    for user in users:
        if user['username'] == username:
            return False
    new_user = {'username': username, 'password': password, 'negara_asal': negara_asal}
    users.append(new_user)
    return True