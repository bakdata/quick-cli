import contextlib
import io

from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import mock_open
from unittest.mock import patch

from quick_client import GatewayCreationData
from quick_client import GatewayDescription
from quick_client import SchemaData

from quick.commands.gateway import ApplyDefinition
from quick.commands.gateway import CreateGateway
from quick.commands.gateway import DeleteGateway
from quick.commands.gateway import DescribeGateway
from quick.commands.gateway import GatewayGroup
from quick.commands.gateway import GatewaySchema
from quick.commands.gateway import ListGateway
from quick.exception import InvalidNameException
from tests.quick.commands.util import check_correct_parser_creation
from tests.quick.commands.util import create_command_in_hierarchy


class TestCreate(TestCase):
    COMMAND = "create"
    NAME = "test-name"
    OPTIONAL = ["--replicas", "--tag", "--schema"]
    REPLICAS = 3
    VERSION = "test_version"
    SCHEMA_FILE = "test.graphql"
    SCHEMA = "type Query { test: String }"
    ERROR_MESSAGE = f"Something went wrong.\nCould not create gateway: {NAME}"

    def setUp(self):
        self.mock_client = Mock()
        self.parser, _ = create_command_in_hierarchy([GatewayGroup, CreateGateway], self.mock_client)

    def test_create_sub_parser(self):
        check_correct_parser_creation(CreateGateway)

    def test_execute_no_optional(self):
        args = self.parser.parse_args(["gateway", self.COMMAND, self.NAME])
        args.func(args)
        expected_data = GatewayCreationData(name=self.NAME)
        self.mock_client.create_gateway.assert_called_once_with(gateway_creation_data=expected_data)

    def test_execute_with_optional_replicas(self):
        args = self.parser.parse_args(["gateway", self.COMMAND, self.NAME, self.OPTIONAL[0], str(self.REPLICAS)])
        args.func(args)
        expected_data = GatewayCreationData(name=self.NAME, replicas=self.REPLICAS)
        self.mock_client.create_gateway.assert_called_once_with(gateway_creation_data=expected_data)

    def test_execute_with_optional_version(self):
        args = self.parser.parse_args(["gateway", self.COMMAND, self.NAME, self.OPTIONAL[1], self.VERSION])
        args.func(args)
        expected_data = GatewayCreationData(name=self.NAME, tag=self.VERSION)
        self.mock_client.create_gateway.assert_called_once_with(gateway_creation_data=expected_data)

    @patch("builtins.open", mock_open(read_data=SCHEMA))
    def test_execute_with_optional_schema(self):
        args = self.parser.parse_args(["gateway", self.COMMAND, self.NAME, self.OPTIONAL[2], self.SCHEMA_FILE])
        args.func(args)
        expected_data = GatewayCreationData(name=self.NAME, schema=self.SCHEMA)
        self.mock_client.create_gateway.assert_called_once_with(gateway_creation_data=expected_data)

    def test_execute_with_non_existing_schema_file(self):
        f = io.StringIO()
        with self.assertRaises(SystemExit) as cm, contextlib.redirect_stderr(f):
            self.parser.parse_args(["gateway", self.COMMAND, self.NAME, self.OPTIONAL[2], self.SCHEMA_FILE])
        self.assertEqual(cm.exception.code, 2)
        self.assertTrue("Error: argument -s/--schema: can't open 'test.graphql':" in f.getvalue())

    @patch("builtins.open", mock_open(read_data=SCHEMA))
    def test_execute_with_optionals(self):
        args = self.parser.parse_args(
            [
                "gateway",
                self.COMMAND,
                self.NAME,
                self.OPTIONAL[0],
                str(self.REPLICAS),
                self.OPTIONAL[1],
                self.VERSION,
                self.OPTIONAL[2],
                "schema.graphql",
            ]
        )
        args.func(args)
        expected_data = GatewayCreationData(
            name=self.NAME, replicas=self.REPLICAS, tag=self.VERSION, schema=self.SCHEMA
        )
        self.mock_client.create_gateway.assert_called_once_with(gateway_creation_data=expected_data)

    def test_invalid_gateway_name(self):
        invalid_name = "gateway_underline_invalid"
        args = self.parser.parse_args(
            [
                "gateway",
                self.COMMAND,
                invalid_name,
                self.OPTIONAL[0],
                str(self.REPLICAS),
                self.OPTIONAL[1],
                self.VERSION,
            ]
        )
        self.assertRaises(InvalidNameException, args.func, args)


class TestUpdate(TestCase):
    COMMAND = "apply"
    NAME = "test_gateway.py"
    FILE_COMMAND = "--file"
    FILE = "tes_file"
    FILE_CONTENT = "data"
    ERROR_MESSAGE = f"Something went wrong.\nCould not apply definition for gateway: {NAME}"

    def setUp(self):
        self.mock_client = Mock()
        self.parser, _ = create_command_in_hierarchy([GatewayGroup, ApplyDefinition], self.mock_client)

    def test_create_sub_parser(self):
        check_correct_parser_creation(ApplyDefinition)

    @patch("builtins.open", mock_open(read_data=FILE_CONTENT))
    def test_execute(self):
        args = self.parser.parse_args(["gateway", self.COMMAND, self.NAME, self.FILE_COMMAND, self.FILE])
        args.func(args)
        self.mock_client.create_schema.assert_called_once_with(self.NAME, SchemaData(self.FILE_CONTENT))

    def test_execute_required_file_field(self):
        f = io.StringIO()
        with self.assertRaises(SystemExit) as cm, contextlib.redirect_stderr(f):
            self.parser.parse_args(["gateway", self.COMMAND, self.NAME])
        self.assertEqual(cm.exception.code, 2)
        self.assertTrue("Error: the following arguments are required: -f/--file" in f.getvalue())


class TestDelete(TestCase):
    COMMAND = "delete"
    NAME = "test-name"

    def setUp(self):
        self.mock_client = Mock()
        self.parser, _ = create_command_in_hierarchy([GatewayGroup, DeleteGateway], self.mock_client)

    def test_create_sub_parser(self):
        check_correct_parser_creation(DeleteGateway)

    def test_execute(self):
        args = self.parser.parse_args(["gateway", self.COMMAND, self.NAME])
        args.func(args)
        self.mock_client.delete_gateway.assert_called_once_with(self.NAME)


class TestList(TestCase):
    COMMAND = "list"

    def setUp(self):
        self.mock_client = Mock()
        self.parser, _ = create_command_in_hierarchy([GatewayGroup, ListGateway], self.mock_client)

    def test_create_sub_parser(self):
        check_correct_parser_creation(ListGateway)

    def test_execute(self):
        args = self.parser.parse_args(["gateway", self.COMMAND])
        self.mock_client.list_all_gateways.return_value = []
        args.func(args)
        self.mock_client.list_all_gateways.assert_called_once_with()


class TestDescribe(TestCase):
    COMMAND = "describe"
    NAME = "test-name"

    def setUp(self):
        self.mock_client = Mock()
        self.parser, _ = create_command_in_hierarchy([GatewayGroup, DescribeGateway], self.mock_client)

    def test_create_sub_parser(self):
        check_correct_parser_creation(DescribeGateway)

    def test_execute(self):
        args = self.parser.parse_args(["gateway", self.COMMAND, self.NAME])
        self.mock_client.get_gateway.return_value = GatewayDescription("", "", "")
        args.func(args)
        self.mock_client.get_gateway.assert_called_once_with(self.NAME)


class TestGatewaySchema(TestCase):
    COMMAND = "schema"
    NAME = "test-name"
    TYPE = "Test"

    def setUp(self):
        self.mock_client = Mock()
        self.parser, _ = create_command_in_hierarchy([GatewayGroup, GatewaySchema], self.mock_client)

    def test_create_sub_parser(self):
        check_correct_parser_creation(GatewaySchema)

    def test_execute_with_graphql_format(self):
        args = self.parser.parse_args(["gateway", self.COMMAND, self.NAME, self.TYPE])
        args.func(args)
        self.mock_client.get_graphql_write_schema.assert_called_once_with(self.NAME, self.TYPE)

    def test_execute_with_avro_format(self):
        args = self.parser.parse_args(["gateway", self.COMMAND, self.NAME, self.TYPE, "--avro"])
        args.func(args)
        self.mock_client.get_avro_write_schema.assert_called_once_with(self.NAME, self.TYPE)
