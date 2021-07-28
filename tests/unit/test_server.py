from src import main

def test_if_server_adduser_add_user_on_server_users_list():
    server = main.Server(1)
    user = main.User(1)

    server.adduser(user)

    assert len(server.users) == 1

def test_if_the_server_userslist_will_be_refreshed():
    server = main.Server(1)
    user = main.User(1)
    user.task = None

    server.adduser(user)
    server.refresh_userlist()

    assert len(server.users) == 0

def test_if_the_server_is_full():
    server = main.Server(1)
    user = main.User(1)

    server.adduser(user)

    assert server.isfull == True

def test_if_server_cant_add_other_user():
    server = main.Server(1)
    user = main.User(1)
    other = main.User(1)

    server.adduser(user)

    if not server.isfull:
        server.adduser(other)

    assert len(server.users) == 1
