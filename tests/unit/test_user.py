from src import main

def test_if_the_user_increase_task_progress():
    user = main.User(3)

    user.increase_task_progress()
    user.increase_task_progress()

    assert user.task["progress"] == 2

def test_if_the_task_closes():
    user = main.User(1)

    user.increase_task_progress()

    assert user.task is None
