from argparse import ArgumentParser
from typing import Iterable
from typing import Tuple
from typing import Type
from unittest.mock import Mock

from quick.commands.base import Command
from quick.commands.base import Group
from quick.commands.base import ManagerCommand
from quick.commands.base import Parsable
from quick.config import QuickConfig
from quick.parser import QuickArgParser
from quick.parser import QuickHelpFormatter


def check_correct_parser_creation(command: Type[Command]):
    mock_sub_parser = Mock()
    command().create_sub_parser(mock_sub_parser)
    mock_sub_parser.add_parser.assert_called_once_with(
        command.name,
        description=command.description or command.help,
        formatter_class=QuickHelpFormatter,
        help=command.help,
    )


def create_command_in_hierarchy(
    parsables: Iterable[Type[Parsable]], client: Mock = None, config: QuickConfig = None
) -> Tuple[ArgumentParser, Parsable]:
    parser = QuickArgParser(
        description="Control your quick deployment.",
        prog="quick",
        formatter_class=QuickHelpFormatter,
    )
    parent = parser.add_subparsers(title="Available commands", metavar="command [options ...]", required=True)
    last_command = None
    for parsable in parsables:
        if issubclass(parsable, Group):
            if hasattr(parsable, "description"):
                description = parsable.description
            else:
                description = parsable.help
            group = parent.add_parser(
                parsable.name,
                description=description,
                help=help,
                formatter_class=QuickHelpFormatter,
            )
            parent = group.add_subparsers(title="Available commands", metavar="command [options ...]")
        elif issubclass(parsable, Command):
            last_command = parsable(config=config)
            parent = last_command.create_sub_parser(parent)

    if last_command is None:
        raise Exception("Command is not initialized!")

    if isinstance(last_command, ManagerCommand):
        last_command.client = client

    return parser, last_command
