# coding: utf-8

"""
    Quick Manager

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import quick_client
from quick_client.models.application_creation_data_arguments import ApplicationCreationDataArguments  # noqa: E501
from quick_client.rest import ApiException

class TestApplicationCreationDataArguments(unittest.TestCase):
    """ApplicationCreationDataArguments unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ApplicationCreationDataArguments
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = quick_client.models.application_creation_data_arguments.ApplicationCreationDataArguments()  # noqa: E501
        if include_optional :
            return ApplicationCreationDataArguments(
                key = '0', 
                value = '0'
            )
        else :
            return ApplicationCreationDataArguments(
        )

    def testApplicationCreationDataArguments(self):
        """Test ApplicationCreationDataArguments"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()