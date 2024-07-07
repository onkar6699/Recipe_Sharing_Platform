# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class InlineObject4(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, username=None, password=None, role=None):  # noqa: E501
        """InlineObject4 - a model defined in OpenAPI

        :param username: The username of this InlineObject4.  # noqa: E501
        :type username: str
        :param password: The password of this InlineObject4.  # noqa: E501
        :type password: str
        :param role: The role of this InlineObject4.  # noqa: E501
        :type role: str
        """
        self.openapi_types = {
            'username': str,
            'password': str,
            'role': str
        }

        self.attribute_map = {
            'username': 'username',
            'password': 'password',
            'role': 'role'
        }

        self._username = username
        self._password = password
        self._role = role

    @classmethod
    def from_dict(cls, dikt) -> 'InlineObject4':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The inline_object_4 of this InlineObject4.  # noqa: E501
        :rtype: InlineObject4
        """
        return util.deserialize_model(dikt, cls)

    @property
    def username(self):
        """Gets the username of this InlineObject4.


        :return: The username of this InlineObject4.
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """Sets the username of this InlineObject4.


        :param username: The username of this InlineObject4.
        :type username: str
        """

        self._username = username

    @property
    def password(self):
        """Gets the password of this InlineObject4.


        :return: The password of this InlineObject4.
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password):
        """Sets the password of this InlineObject4.


        :param password: The password of this InlineObject4.
        :type password: str
        """

        self._password = password

    @property
    def role(self):
        """Gets the role of this InlineObject4.


        :return: The role of this InlineObject4.
        :rtype: str
        """
        return self._role

    @role.setter
    def role(self, role):
        """Sets the role of this InlineObject4.


        :param role: The role of this InlineObject4.
        :type role: str
        """
        allowed_values = ["admin", "contributor"]  # noqa: E501
        if role not in allowed_values:
            raise ValueError(
                "Invalid value for `role` ({0}), must be one of {1}"
                .format(role, allowed_values)
            )

        self._role = role