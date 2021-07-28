#!/usr/bin/env python3

"""
challenge topaz - load balancing servers calculator

Author: Gabriel Fonseca <fonsecacrz7@gmail.com>

---

this script makes the server calculation cost based in a `.txt` input file to
reduce server's costs

Usage:

    $ ./main.py
    or
    $ python main.py

obs: to change input/ output just modify `INPUTFILE` and `OUTPUTFILE` variables

History:

    v1.0.0 2021-07-27, Gabriel Fonseca:
        - initial version

License: MIT
"""

from __future__ import annotations
import typing as T
import math

SERVER_COST = 1
INPUTFILE = "simulations/input.txt"
OUTPUTFILE = "simulations/output.txt"


class Server:
    """
    Server abstraction

    Attributes:
        - capacity (int): max simultaneous users in the server (umax)
        - users (list): list of users inside the server
        - isfull (bool): checks if the server is full

    Methods:
        - adduser: add a new user on the server
        - refresh_userlist: clear users without tasks on server
    """

    users: T.List[User]

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.users = []

    def adduser(self, user: User) -> None:
        """
        Called when is necessary add a new user's process

        Arguments:
            - user (user): a user abstraction
        """

        self.users.append(user)

    def refresh_userlist(self) -> None:
        """Called when it's necessary to make checks of users without tasks"""

        self.users = [user for user in self.users if user.task is not None]

    @property
    def isfull(self) -> bool:
        """
        Called when it's necessary valid the server's state

        Returns:
            bool: True if the server is full, otherwise False
        """

        return True if len(self.users) == self.capacity else False


class User:
    """
    User abstraction

    Attributes:
        - task: the user's task

    Methods:
        - increase_task_progress: changes the user's task progress
    """

    task: T.Dict[str, int]

    def __init__(self, ttask: int):
        self.task = dict(ttask=ttask, progress=0)

    def increase_task_progress(self) -> None:
        """Called when the server process the task"""

        self.task["progress"] += 1

        if self.task["progress"] == self.task["ttask"]:
            self.task = None


class InvalidTtaskValue(Exception):
    pass


class InvalidUmaxValue(Exception):
    pass


def genoutput(line: T.List[int]) -> None:
    """
    Generate a line logging on the output file

    Arguments:
        - line (list): a list of server with quantity of users inside each
    """

    with open(OUTPUTFILE, "a") as output:
        for i, user in enumerate(line):
            output.write(str(user))

            try:
                _next = line[i + 1]

                if _next:
                    output.write(",")
            except IndexError:
                continue

        output.write("\n")


def main(payload: T.List[int]) -> None:
    """
    Main function

    Arguments:
        - payload (list): list with task/ server and users infos

    Exceptions:
        - InvalidTtaskValue: raised when the value of `ttask` is invalid
        - InvalidUmaxValue: raised when the value of `umax` is invalid

    Business Rules:
        - 1 <= ttask <= 10
        - 1 <= umax <= 10
    """

    [ttask, umax, *new_users] = payload

    if not 1 <= ttask <= 10:
        raise InvalidTtaskValue(f"invalid ttask value: {ttask}")

    if not 1 <= umax <= 10:
        raise InvalidUmaxValue(f"invalid umax value: {umax}")

    cost = 0
    servers: T.List[Server] = []

    while True:
        try:
            quantity = new_users.pop(0)
        except IndexError:
            quantity = 0

        for _ in range(quantity):
            user = User(ttask)
            added = False

            for server in servers:
                if not server.isfull:
                    server.adduser(user)
                    added = True

            if not added:
                server = Server(umax)
                server.adduser(user)
                servers.append(server)

        for server in servers:
            [
                user.increase_task_progress()
                for user in server.users if user.task
            ]

        cost += SERVER_COST * len(servers)

        genoutput([len(server.users) for server in servers])

        [server.refresh_userlist() for server in servers]
        servers = [server for server in servers if len(server.users) > 0]

        if len(servers) == 0:
            break

    return cost


def entrypoint():
    """a main function wrapper to makes test easily"""

    with open(INPUTFILE, "r") as file:
        payload = [int(line) for line in file.read().split("\n")[:-1]]

    cost = main(payload)

    genoutput([0])
    genoutput([cost])


if __name__ == "__main__":
    entrypoint()

