import contextlib
import io
import sys

from unittest import TestCase
from unittest.mock import Mock

from quick_client import GatewaySchema
from quick_client import TopicCreationData
from quick_client import TopicData
from quick_client import TopicWriteType

from quick.commands.topic import CreateTopic
from quick.commands.topic import DeleteTopic
from quick.commands.topic import DescribeTopic
from quick.commands.topic import ListTopic
from quick.commands.topic import TopicGroup
from tests.quick.commands.util import check_correct_parser_creation
from tests.quick.commands.util import create_command_in_hierarchy


class TestTopic(TestCase):
    COMMAND = "create"
    NAME = "test-topic"
    KEY_CMD = "--key-type"
    KEY_TYPE = "string"
    VALUE_CMD = "--value-type"
    VALUE_TYPE = "schema"
    SCHEMA_CMD = "--schema"
    SCHEMA = "testGateway.testType"
    GATEWAY_SCHEMA = GatewaySchema("testGateway", "testType")

    ERROR_MESSAGE = f"Something went wrong.\nCould not create new topic: {NAME}"

    NO_TOPICS_EXISTS_MESSAGE = (
        "There are no topics registered. " "Please create one using quick topic create <NAME> -k <TYPE> -v <TYPE>"
    )

    def setUp(self):
        self.mock_client = Mock()
        self.parser, _ = create_command_in_hierarchy([TopicGroup, CreateTopic], self.mock_client)

    def test_create_sub_parser(self):
        check_correct_parser_creation(CreateTopic)

    def test_execute(self):
        creation_data = TopicCreationData(write_type=TopicWriteType.MUTABLE, value_schema=self.GATEWAY_SCHEMA)

        args = self.parser.parse_args(
            [
                "topic",
                self.COMMAND,
                self.NAME,
                self.KEY_CMD,
                self.KEY_TYPE,
                self.VALUE_CMD,
                self.VALUE_TYPE,
                self.SCHEMA_CMD,
                self.SCHEMA,
            ]
        )
        args.func(args)

        self.mock_client.create_new_topic.assert_called_once_with(
            "test-topic",
            key_type=self.KEY_TYPE,
            topic_creation_data=creation_data,
            value_type="schema",
        )

    def test_execute_immutable(self):
        creation_data = TopicCreationData(write_type=TopicWriteType.IMMUTABLE, value_schema=self.GATEWAY_SCHEMA)

        args = self.parser.parse_args(
            [
                "topic",
                self.COMMAND,
                self.NAME,
                self.KEY_CMD,
                self.KEY_TYPE,
                self.VALUE_CMD,
                self.VALUE_TYPE,
                self.SCHEMA_CMD,
                self.SCHEMA,
                "--immutable",
            ]
        )

        args.func(args)

        self.mock_client.create_new_topic.assert_called_once_with(
            "test-topic",
            key_type=self.KEY_TYPE,
            topic_creation_data=creation_data,
            value_type="schema",
        )

    def test_execute_retention_time(self):
        creation_data = TopicCreationData(
            write_type=TopicWriteType.MUTABLE,
            value_schema=self.GATEWAY_SCHEMA,
            retention_time="PT5M",
        )
        args = self.parser.parse_args(
            [
                "topic",
                self.COMMAND,
                self.NAME,
                self.KEY_CMD,
                self.KEY_TYPE,
                self.VALUE_CMD,
                self.VALUE_TYPE,
                self.SCHEMA_CMD,
                self.SCHEMA,
                "--retention-time",
                "PT5M",
            ]
        )
        args.func(args)

        self.mock_client.create_new_topic.assert_called_once_with(
            "test-topic",
            key_type=self.KEY_TYPE,
            topic_creation_data=creation_data,
            value_type="schema",
        )

    def test_execute_required_key_value_type_field(self):
        f = io.StringIO()
        with self.assertRaises(SystemExit) as cm, contextlib.redirect_stderr(f):
            self.parser.parse_args(["topic", self.COMMAND, self.NAME])
        self.assertEqual(cm.exception.code, 2)
        self.assertTrue("Error: the following arguments are required: -k/--key-type, -v/--value-type" in f.getvalue())

    def test_execute_range(self):
        creation_data = TopicCreationData(
            write_type=TopicWriteType.MUTABLE, value_schema=self.GATEWAY_SCHEMA, point=False, range_field="testField"
        )

        args = self.parser.parse_args(
            [
                "topic",
                self.COMMAND,
                self.NAME,
                self.KEY_CMD,
                self.KEY_TYPE,
                self.VALUE_CMD,
                self.VALUE_TYPE,
                self.SCHEMA_CMD,
                self.SCHEMA,
                "--no-point",
                "--range-field",
                "testField",
            ]
        )
        args.func(args)

        self.mock_client.create_new_topic.assert_called_once_with(
            "test-topic", key_type=self.KEY_TYPE, topic_creation_data=creation_data, value_type="schema"
        )


class TestDelete(TestCase):
    COMMAND = "delete"
    NAME = "test_name"

    def setUp(self):
        self.mock_client = Mock()
        self.parser, _ = create_command_in_hierarchy([TopicGroup, DeleteTopic], self.mock_client)

    def test_create_sub_parser(self):
        check_correct_parser_creation(DeleteTopic)

    def test_delete_topic(self):
        args = self.parser.parse_args(["topic", self.COMMAND, self.NAME])
        args.func(args)
        self.mock_client.delete_topic.assert_called_once_with(self.NAME)


class TestList(TestCase):
    COMMAND = "topic"
    NAME = "test-topic"

    def setUp(self):
        self.mock_client = Mock()
        self.parser, _ = create_command_in_hierarchy([TopicGroup, ListTopic], self.mock_client)

    def test_list_topics(self):
        list_topic = [
            TopicData("test-topic-1", "", "", ""),
            TopicData("test-topic-2", "", "", ""),
        ]
        self.mock_client.list_all_topics.return_value = list_topic

        captured_output = io.StringIO()
        sys.stdout = captured_output
        args = self.parser.parse_args([self.COMMAND, "list"])
        with contextlib.redirect_stdout(captured_output):
            args.func(args)
        captured_values = captured_output.getvalue().split("\n")[:-1]
        self.assertEqual(len(list_topic), len(captured_values))


class TestDescribe(TestCase):
    COMMAND = "topic"
    NAME = "test-topic"

    def setUp(self):
        self.mock_client = Mock()
        self.parser, _ = create_command_in_hierarchy([TopicGroup, DescribeTopic], self.mock_client)

    def test_describe_topic(self):
        list_topics = [
            TopicData("test-topic-1", "test_type", "test_type", "test_type"),
            TopicData("test-topic-2", "", "", ""),
        ]

        describe_topic = list_topics[0]

        captured_values = self.__describe_topic(describe_topic)

        actual_value = (
            f"Name: {describe_topic.name}\n"
            f"Key Type: {describe_topic.key_type}\n"
            f"Value Type: {describe_topic.value_type}\n"
            f"Write Type: {describe_topic.write_type}"
        )

        self.assertEqual(actual_value, captured_values)

    def test_describe_topic_with_schema(self):
        list_topics = [
            TopicData("test-topic-1", "test_type", "test_type", "test_type", "schema"),
            TopicData("test-topic-2", "", "", ""),
        ]

        describe_topic = list_topics[0]

        captured_values = self.__describe_topic(describe_topic)

        actual_value = (
            f"Name: {describe_topic.name}\n"
            f"Key Type: {describe_topic.key_type}\n"
            f"Value Type: {describe_topic.value_type}\n"
            f"Write Type: {describe_topic.write_type}\n"
            f"Schema:\n{describe_topic.schema}"
        )
        self.assertEqual(actual_value, captured_values)

    def __describe_topic(self, describe_topic: TopicData):
        self.mock_client.get_topic_information.return_value = describe_topic
        captured_output = io.StringIO()
        sys.stdout = captured_output
        args = self.parser.parse_args([self.COMMAND, "describe", describe_topic.name])
        with contextlib.redirect_stdout(captured_output):
            args.func(args)
        return captured_output.getvalue()[:-1]
