# coding: utf-8

"""
    Quick Manager

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from quick_client.configuration import Configuration


class MirrorArguments(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'retention_time': 'str',
        'range_field': 'str',
        'range_key': 'str'
    }

    attribute_map = {
        'retention_time': 'retentionTime',
        'range_field': 'rangeField',
        'range_key': 'rangeKey'
    }

    def __init__(self, retention_time=None, range_field=None, range_key=None, local_vars_configuration=None):  # noqa: E501
        """MirrorArguments - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._retention_time = None
        self._range_field = None
        self._range_key = None
        self.discriminator = None

        if retention_time is not None:
            self.retention_time = retention_time
        if range_field is not None:
            self.range_field = range_field
        if range_key is not None:
            self.range_key = range_key

    @property
    def retention_time(self):
        """Gets the retention_time of this MirrorArguments.  # noqa: E501


        :return: The retention_time of this MirrorArguments.  # noqa: E501
        :rtype: str
        """
        return self._retention_time

    @retention_time.setter
    def retention_time(self, retention_time):
        """Sets the retention_time of this MirrorArguments.


        :param retention_time: The retention_time of this MirrorArguments.  # noqa: E501
        :type: str
        """

        self._retention_time = retention_time

    @property
    def range_field(self):
        """Gets the range_field of this MirrorArguments.  # noqa: E501


        :return: The range_field of this MirrorArguments.  # noqa: E501
        :rtype: str
        """
        return self._range_field

    @range_field.setter
    def range_field(self, range_field):
        """Sets the range_field of this MirrorArguments.


        :param range_field: The range_field of this MirrorArguments.  # noqa: E501
        :type: str
        """

        self._range_field = range_field

    @property
    def range_key(self):
        """Gets the range_key of this MirrorArguments.  # noqa: E501


        :return: The range_key of this MirrorArguments.  # noqa: E501
        :rtype: str
        """
        return self._range_key

    @range_key.setter
    def range_key(self, range_key):
        """Sets the range_key of this MirrorArguments.


        :param range_key: The range_key of this MirrorArguments.  # noqa: E501
        :type: str
        """

        self._range_key = range_key

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, MirrorArguments):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, MirrorArguments):
            return True

        return self.to_dict() != other.to_dict()
