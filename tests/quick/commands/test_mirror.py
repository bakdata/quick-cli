from unittest import TestCase
from unittest.mock import Mock

from quick_client import MirrorCreationData

from quick.commands.mirror import CreateMirror
from quick.commands.mirror import DeleteMirror
from quick.commands.mirror import MirrorGroup
from tests.quick.commands.util import check_correct_parser_creation
from tests.quick.commands.util import create_command_in_hierarchy


class TestDelete(TestCase):
    COMMAND = "delete"
    NAME = "test-name"

    def setUp(self):
        self.mock_client = Mock()
        self.parser, _ = create_command_in_hierarchy([MirrorGroup, DeleteMirror], self.mock_client)

    def test_create_sub_parser(self):
        check_correct_parser_creation(DeleteMirror)

    def test_delete_mirror(self):
        args = self.parser.parse_args(["mirror", self.COMMAND, self.NAME])
        args.func(args)
        self.mock_client.delete_mirror.assert_called_once_with(self.NAME)


class TestMirror(TestCase):
    COMMAND = "create"
    OPTIONAL = ["--replicas", "--tag", "--point", "--range-field"]
    TOPIC = "test_topic"
    REPLICAS = 3
    VERSION = "test_version"
    RANGE_FILED = "testField"
    ERROR_MESSAGE = f"Something went wrong.\nCould not create mirror for topic: {TOPIC}"

    def setUp(self):
        self.mock_client = Mock()
        self.parser, self.mirror = create_command_in_hierarchy([MirrorGroup, CreateMirror], self.mock_client)

    def test_create_sub_parser(self):
        check_correct_parser_creation(CreateMirror)

    def test_execute_no_optional(self):
        args = self.parser.parse_args(["mirror", self.COMMAND, self.TOPIC])
        args.func(args)
        expected_data = MirrorCreationData(self.TOPIC, self.TOPIC, replicas=1, tag=None, point=True, range_field=None)
        self.mock_client.create_mirror.assert_called_once_with(mirror_creation_data=expected_data)

    def test_execute_with_optional_replicas(self):
        args = self.parser.parse_args(["mirror", self.COMMAND, self.TOPIC, self.OPTIONAL[0], str(self.REPLICAS)])
        args.func(args)
        expected_data = MirrorCreationData(self.TOPIC, self.TOPIC, replicas=self.REPLICAS, tag=None)
        self.mock_client.create_mirror.assert_called_once_with(mirror_creation_data=expected_data)

    def test_execute_with_optional_version(self):
        args = self.parser.parse_args(["mirror", self.COMMAND, self.TOPIC, self.OPTIONAL[1], self.VERSION])
        args.func(args)
        expected_data = MirrorCreationData(self.TOPIC, self.TOPIC, replicas=1, tag=self.VERSION)
        self.mock_client.create_mirror.assert_called_once_with(mirror_creation_data=expected_data)

    def test_execute_with_optionals(self):
        args = self.parser.parse_args(
            [
                "mirror",
                self.COMMAND,
                self.TOPIC,
                self.OPTIONAL[0],
                str(self.REPLICAS),
                self.OPTIONAL[1],
                self.VERSION,
                self.OPTIONAL[2],
                self.OPTIONAL[3],
                self.RANGE_FILED,
            ]
        )
        args.func(args)
        expected_data = MirrorCreationData(
            self.TOPIC, self.TOPIC, replicas=self.REPLICAS, tag=self.VERSION, point=True, range_field=self.RANGE_FILED
        )
        self.mock_client.create_mirror.assert_called_once_with(mirror_creation_data=expected_data)
