import os
import tempfile

from pathlib import Path
from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch

from quick.commands.context import ActivateContext
from quick.commands.context import ContextGroup
from quick.commands.context import CreateContext
from quick.commands.context import DescribeContext
from quick.commands.context import ListContexts
from quick.config import QuickConfig
from tests.quick.commands.util import check_correct_parser_creation
from tests.quick.commands.util import create_command_in_hierarchy


class TestCreate(TestCase):
    COMMAND = "create"
    HOST = "https://dev.d9p.io"
    API_KEY = "test_key"
    CONTEXT_NAME = "dev"
    HOST_WITH_SLASH = "https://dev.d9p.io/"

    def setUp(self):
        self.mock_client = Mock()
        self.config_file = tempfile.NamedTemporaryFile(delete=False)
        self.config = QuickConfig(config_path=Path(self.config_file.name))
        self.parser, _ = create_command_in_hierarchy([ContextGroup, CreateContext], config=self.config)

    def test_create_sub_parser(self):
        check_correct_parser_creation(CreateContext)

    @patch("builtins.input", return_value=HOST)
    @patch("getpass.getpass", return_value=API_KEY)
    def test_execute(self, *args):
        args = self.parser.parse_args(["context", self.COMMAND])
        args.func(args)
        assert self.HOST + "/manager" == self.config.get_host()
        assert self.API_KEY == self.config.get_api_key()

    @patch("builtins.input", return_value=HOST_WITH_SLASH)
    @patch("getpass.getpass", return_value=API_KEY)
    def test_execute_with_extra_slash(self, *args):
        args = self.parser.parse_args(["context", self.COMMAND])
        args.func(args)
        assert self.HOST + "/manager" == self.config.get_host()
        assert self.API_KEY == self.config.get_api_key()

    def test_execute_with_flags(self):
        self.parser, _ = create_command_in_hierarchy([ContextGroup, CreateContext], config=self.config)

        args = self.parser.parse_args(
            ["context", self.COMMAND, "--host", self.HOST, "--key", self.API_KEY, "--context", self.CONTEXT_NAME]
        )
        args.func(args)
        assert self.HOST + "/manager" == self.config.get_host()
        assert self.API_KEY == self.config.get_api_key()

    def tearDown(self) -> None:
        self.config_file.close()
        os.unlink(self.config_file.name)


class TestList(TestCase):
    COMMAND = "list"
    HOSTS = ["https://dev.d9p.io", "https://demo.d9p.io"]
    API_KEYS = ["dev_key", "demo_key"]
    CONTEXT_NAMES = ["dev", "demo"]

    def setUp(self):
        self.config = Mock()

    def test_create_sub_parser(self):
        check_correct_parser_creation(ListContexts)

    def test_execute(self):
        self.config.get_all.return_value = {
            self.CONTEXT_NAMES[0]: {"apiKey": self.API_KEYS[0], "host": self.HOSTS[0]},
            self.CONTEXT_NAMES[1]: {"apiKey": self.API_KEYS[1], "host": self.HOSTS[1]},
        }
        self.config.get_current_context.return_value = self.CONTEXT_NAMES[0]
        self.parser, _ = create_command_in_hierarchy([ContextGroup, ListContexts], config=self.config)
        args = self.parser.parse_args(["context", self.COMMAND])
        args.func(args)
        self.config.get_all.assert_called_once_with()


class TestActivateContext(TestCase):
    COMMAND = "activate"
    CONTEXT_NAME = "demo"

    def setUp(self):
        self.config = Mock()

    def test_create_sub_parser(self):
        check_correct_parser_creation(ActivateContext)

    def test_execute(self):
        self.parser, _ = create_command_in_hierarchy([ContextGroup, ActivateContext], config=self.config)
        args = self.parser.parse_args(["context", self.COMMAND, self.CONTEXT_NAME])
        args.func(args)
        self.config.set_current_context.assert_called_once_with(self.CONTEXT_NAME)


class TestDescribeContext(TestCase):
    COMMAND = "describe"
    CONTEXT_NAME = "demo"

    def setUp(self):
        self.config = Mock()

    def test_create_sub_parser(self):
        check_correct_parser_creation(DescribeContext)

    def test_execute_no_flag(self):
        self.config.get_current_context.return_value = self.CONTEXT_NAME
        self.config.get_current_context_config.return_value = self.CONTEXT_NAME
        self.parser, _ = create_command_in_hierarchy([ContextGroup, DescribeContext], config=self.config)
        args = self.parser.parse_args(["context", self.COMMAND])
        args.func(args)
        self.config.get_current_context_config.assert_called_once_with(self.CONTEXT_NAME)

    def test_execute_with_flag(self):
        self.config.get_current_context_config.return_value = self.CONTEXT_NAME
        self.parser, _ = create_command_in_hierarchy([ContextGroup, DescribeContext], config=self.config)
        args = self.parser.parse_args(["context", self.COMMAND, "--context", self.CONTEXT_NAME])
        args.func(args)
        self.config.get_current_context_config.assert_called_once_with(self.CONTEXT_NAME)
