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
from quick_client.models.topic_creation_data import TopicCreationData  # noqa: E501
from quick_client.rest import ApiException

class TestTopicCreationData(unittest.TestCase):
    """TopicCreationData unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test TopicCreationData
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = quick_client.models.topic_creation_data.TopicCreationData()  # noqa: E501
        if include_optional :
            return TopicCreationData(
                write_type = 'MUTABLE', 
                value_schema = quick_client.models.gateway_schema.GatewaySchema(
                    gateway = '0', 
                    type = '0', ), 
                key_schema = quick_client.models.gateway_schema.GatewaySchema(
                    gateway = '0', 
                    type = '0', ), 
                retention_time = '0', 
                point = True, 
                range_field = '0'
            )
        else :
            return TopicCreationData(
        )

    def testTopicCreationData(self):
        """Test TopicCreationData"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
