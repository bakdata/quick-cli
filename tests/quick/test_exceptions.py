from http import HTTPStatus
from unittest import TestCase

from quick_client import ApiException

from quick.exception import InvalidApiKeyException
from quick.exception import ManagerException
from quick.exception import handle_error


TEST_ERROR_JSON = """{
    "type": "test",
    "title": "testTitle",
    "code": 0,
    "detail": "testDetail",
    "uriPath": "testUriPath"
}"""


class TestApiExceptionHandler(TestCase):
    def test_handle_error_internal_server_error(self):
        personal_message = "test personal error message."
        error_message = f"testTitle: testDetail\n{personal_message}"
        api_exception = ApiException(HTTPStatus.INTERNAL_SERVER_ERROR)
        api_exception.body = TEST_ERROR_JSON
        with self.assertRaises(ManagerException) as context:
            handle_error(api_exception, personal_message)
            self.assertEqual(context.exception.message, error_message)

    def test_handle_unauthorized_status(self):
        with self.assertRaises(InvalidApiKeyException):
            api_exception = ApiException(HTTPStatus.UNAUTHORIZED)
            api_exception.body = TEST_ERROR_JSON
            handle_error(api_exception)
