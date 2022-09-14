from unittest import TestCase
from unittest.mock import Mock

from quick_client import ApplicationCreationData

from quick.commands import StreamsAppGroup
from quick.commands.streams_app import DeleteStreamsApp
from quick.commands.streams_app import DeployStreamsApp
from tests.quick.commands.util import check_correct_parser_creation
from tests.quick.commands.util import create_command_in_hierarchy


class TestDeploy(TestCase):
    COMMAND = "deploy"
    OPTIONAL = ["--args", "--replicas", "--image-pull-secret"]
    NAME = "test_app"
    REGISTRY = "https://hub.docker.com/"
    PRIVATE_REGISTRY = "https://hub.docker.com/"
    IMAGE = "test_image"
    REPLICAS = 3
    PORT = 8080
    TAG = "test_tag"
    PULL_SECRET = "secret"
    ARGS = {
        "input-topics": "purchase-topic",
        "output-topic": "purchases-count",
        "count-field": "productId",
    }
    ERROR_MESSAGE = "Something went wrong.\nCould not create application: None"

    def setUp(self):
        self.mock_client = Mock()
        self.parser, _ = create_command_in_hierarchy([StreamsAppGroup, DeployStreamsApp], self.mock_client)

    def test_create_sub_parser(self):
        check_correct_parser_creation(DeployStreamsApp)

    def test_execute_deploy_application_no_args(self):
        args = self.parser.parse_args(
            ["app", self.COMMAND, self.NAME, "--image", self.IMAGE, "--tag", self.TAG, "--registry", self.REGISTRY]
        )
        args.func(args)

        expected = ApplicationCreationData(
            name=self.NAME,
            registry=self.REGISTRY,
            image_name=self.IMAGE,
            tag=self.TAG,
            replicas=1,
            port=None,
            arguments={},
        )

        self.mock_client.deploy_application.assert_called_once_with(application_creation_data=expected)

    def test_execute_deploy_application_with_args(self):
        args_list = list(map(lambda k: k[0] + "=" + k[1], self.ARGS.items()))
        args = self.parser.parse_args(
            [
                "app",
                self.COMMAND,
                self.NAME,
                "--image",
                self.IMAGE,
                "--tag",
                self.TAG,
                "--registry",
                self.REGISTRY,
                self.OPTIONAL[0],
                *args_list,
            ]
        )
        args.func(args)

        expected = ApplicationCreationData(
            name=self.NAME,
            registry=self.REGISTRY,
            image_name=self.IMAGE,
            tag=self.TAG,
            replicas=1,
            port=None,
            arguments=self.ARGS,
        )

        self.mock_client.deploy_application.assert_called_once_with(application_creation_data=expected)

    def test_execute_deploy_application_with_optional_replicas(self):
        args = self.parser.parse_args(
            [
                "app",
                self.COMMAND,
                self.NAME,
                "--image",
                self.IMAGE,
                "--registry",
                self.REGISTRY,
                "--tag",
                self.TAG,
                self.OPTIONAL[1],
                str(self.REPLICAS),
            ]
        )
        args.func(args)

        expected = ApplicationCreationData(
            name=self.NAME,
            registry=self.REGISTRY,
            image_name=self.IMAGE,
            tag=self.TAG,
            replicas=self.REPLICAS,
            port=None,
            arguments={},
        )

        self.mock_client.deploy_application.assert_called_once_with(application_creation_data=expected)

    def test_execute_deploy_application_with_optional_port(self):
        args = self.parser.parse_args(
            [
                "app",
                self.COMMAND,
                self.NAME,
                "--image",
                self.IMAGE,
                "--registry",
                self.REGISTRY,
                "--tag",
                self.TAG,
                "--port",
                str(self.PORT),
            ]
        )
        args.func(args)

        expected = ApplicationCreationData(
            name=self.NAME,
            registry=self.REGISTRY,
            image_name=self.IMAGE,
            tag=self.TAG,
            replicas=1,
            port=self.PORT,
            arguments={},
        )

        self.mock_client.deploy_application.assert_called_once_with(application_creation_data=expected)

    def test_execute_deploy_application_with_image_pull_secret(self):
        args = self.parser.parse_args(
            [
                "app",
                self.COMMAND,
                self.NAME,
                "--image",
                self.IMAGE,
                "--registry",
                self.PRIVATE_REGISTRY,
                "--tag",
                self.TAG,
                "--image-pull-secret",
                self.PULL_SECRET,
                "--port",
                str(self.PORT),
            ]
        )
        args.func(args)

        expected = ApplicationCreationData(
            name=self.NAME,
            registry=self.REGISTRY,
            image_name=self.IMAGE,
            tag=self.TAG,
            image_pull_secret=self.PULL_SECRET,
            replicas=1,
            port=self.PORT,
            arguments={},
        )

        self.mock_client.deploy_application.assert_called_once_with(application_creation_data=expected)


class TestArgParse(TestCase):
    def setUp(self):
        self.mock_client = Mock()
        self.parser, _ = create_command_in_hierarchy([StreamsAppGroup, DeployStreamsApp], self.mock_client)

    def test_parse_map_type_args(self):
        app_args = {
            "input-topics": "purchase-topic",
            "output-topic": "purchases-count",
            "extra-input-topics": "metadata=purchase-metadata-topic,media=purchase-media-topic",
        }
        args_list = list(map(lambda k: k[0] + "=" + k[1], app_args.items()))
        args = self.parser.parse_args(
            [
                "app",
                "deploy",
                "app-with-map-args",
                "--image",
                "test_image",
                "--registry",
                "test_registry",
                "--tag",
                "test_tag",
                "--args",
                *args_list,
            ]
        )
        self.assertDictEqual(args.props, app_args)


class TestDelete(TestCase):
    COMMAND = "delete"
    NAME = "test_name"

    def setUp(self):
        self.mock_client = Mock()
        self.parser, _ = create_command_in_hierarchy([StreamsAppGroup, DeleteStreamsApp], self.mock_client)

    def test_create_sub_parser(self):
        check_correct_parser_creation(DeleteStreamsApp)

    def test_delete_application(self):
        args = self.parser.parse_args(["app", self.COMMAND, self.NAME])
        args.func(args)
        self.mock_client.delete_application.assert_called_once_with(name=self.NAME)
