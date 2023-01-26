import json

from typing import Any as _Any
from dataclasses import dataclass as _dc, field as _field

from pygame_multiplayer.models import ClientBase as _ClientBase


class BaseCommand:
    def __init__(self, flag: int, **kwargs):
        """
        Initializes all the variables in the class and prepares them for use.

        Base Class of any command that is sent/received from/to the server or client.

        Parameters
        ----------
        flag: int
            The flag of the command
        kwargs
            The arguments of the command
        """
        self.flag = flag
        self.args = kwargs

    def __repr__(self):
        return f"<BaseCommand [{self.flag}] args: {', '.join(self.args.keys())})>"

    def serialize(self) -> str:
        """
        Serializes the command into a string

        Returns
        -------
        str
            The serialized command
        """
        return json.dumps(self.__dict__)

    @classmethod
    def deserialize(cls, serial: str) -> "BaseCommand":
        """
        Deserializes a string into a command

        Parameters
        ----------
        serial: str
            The serialized command

        Returns
        -------
        BaseCommand
            The deserialized command
        """
        data = json.loads(serial)
        return cls(data.get("flag"), **data.get("args", {}))


class ClientCommand(BaseCommand):
    """
    Client-Side (Client) Command

    Instance that reprs a command that is sent from the client to the server
    """
    def __repr__(self):
        return f"<ClientCommand [{self.flag}] args: {', ', join(self.args.keys())})>"


class ServerCommand(BaseCommand):
    """
    Client-Side (Server) Command

    Instance that reprs a command that is sent from the server to the client
    """
    def __repr__(self):
        return f"<ServerCommand [{self.flag}] args: {', ', join(self.args.keys())})>"


class ServerSideClientCommand(BaseCommand):
    def __init__(self, flag: int, client: _ClientBase, **kwargs):
        """
        Initializes all the variables in the class and prepares them for use.

        Server-Side (Client) Command
        Instance that reprs a command that is sent from the client to a server

        Parameters
        ----------
        flag : int
            The flag for the command
        client : ClientBase
            The client that sent the command
        kwargs
            The arguments sent from the client
        """
        super().__init__(flag, **kwargs)
        self.client: _ClientBase = client

    def __repr__(self):
        return f"<ServerSideClientCommand [{self.flag}] args: {', '.join(self.args.keys())})>"

    @classmethod
    def from_client_cmd(cls, cmd: BaseCommand, client: _ClientBase) -> "ServerSideClientCommand":
        """
        Creates a ServerSideClientCommand from a ClientCommand

        Parameters
        ----------
        cmd: BaseCommand
            The Command the client sent
        client: ClientBase
            The client that sent the command

        Returns
        -------
        ServerSideClientCommand
            The Command including the object of the client that sent it
        """
        return cls(cmd.flag, client, **cmd.args)


class ServerSideServerCommand(BaseCommand):
    def __init__(self, flag: int, client: _ClientBase, **kwargs):
        """
        Initializes all the variables in the class and prepares them for use.

        Server-Side (Server) Command
        Instance that reprs a command that is sent from the server to a client

        Parameters
        ----------
        flag: int
            The flag of the command
        client: ClientBase
            The client that the command is being sent to
        kwargs
            Additional arguments to be sent with the command
        """
        super().__init__(flag, **kwargs)
        self.client: _ClientBase = client

    def __repr__(self):
        return f"<ServerSideServerCommand [{self.flag}] args: {', ',join(self.args.keys())})>"

    def to_client_cmd(self) -> ServerCommand:
        """
        Creates a ServerCommand from a ServerSideServerCommand

        Returns
        -------
        ServerCommand
            The Command without the object of the client that will be sent to the client
        """
        return ServerCommand(self.flag, **self.args)
