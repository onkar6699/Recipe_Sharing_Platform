# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class Recipe(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, author_id=None, title=None, description=None, ingredients=None, instructions=None, created_at=None):  # noqa: E501
        """Recipe - a model defined in OpenAPI

        :param id: The id of this Recipe.  # noqa: E501
        :type id: int
        :param author_id: The author_id of this Recipe.  # noqa: E501
        :type author_id: int
        :param title: The title of this Recipe.  # noqa: E501
        :type title: str
        :param description: The description of this Recipe.  # noqa: E501
        :type description: str
        :param ingredients: The ingredients of this Recipe.  # noqa: E501
        :type ingredients: List[str]
        :param instructions: The instructions of this Recipe.  # noqa: E501
        :type instructions: str
        :param created_at: The created_at of this Recipe.  # noqa: E501
        :type created_at: datetime
        """
        self.openapi_types = {
            'id': int,
            'author_id': int,
            'title': str,
            'description': str,
            'ingredients': List[str],
            'instructions': str,
            'created_at': datetime
        }

        self.attribute_map = {
            'id': 'id',
            'author_id': 'author_id',
            'title': 'title',
            'description': 'description',
            'ingredients': 'ingredients',
            'instructions': 'instructions',
            'created_at': 'created_at'
        }

        self._id = id
        self._author_id = author_id
        self._title = title
        self._description = description
        self._ingredients = ingredients
        self._instructions = instructions
        self._created_at = created_at

    @classmethod
    def from_dict(cls, dikt) -> 'Recipe':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Recipe of this Recipe.  # noqa: E501
        :rtype: Recipe
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this Recipe.


        :return: The id of this Recipe.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Recipe.


        :param id: The id of this Recipe.
        :type id: int
        """

        self._id = id

    @property
    def author_id(self):
        """Gets the author_id of this Recipe.


        :return: The author_id of this Recipe.
        :rtype: int
        """
        return self._author_id

    @author_id.setter
    def author_id(self, author_id):
        """Sets the author_id of this Recipe.


        :param author_id: The author_id of this Recipe.
        :type author_id: int
        """

        self._author_id = author_id

    @property
    def title(self):
        """Gets the title of this Recipe.


        :return: The title of this Recipe.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this Recipe.


        :param title: The title of this Recipe.
        :type title: str
        """

        self._title = title

    @property
    def description(self):
        """Gets the description of this Recipe.


        :return: The description of this Recipe.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Recipe.


        :param description: The description of this Recipe.
        :type description: str
        """

        self._description = description

    @property
    def ingredients(self):
        """Gets the ingredients of this Recipe.


        :return: The ingredients of this Recipe.
        :rtype: List[str]
        """
        return self._ingredients

    @ingredients.setter
    def ingredients(self, ingredients):
        """Sets the ingredients of this Recipe.


        :param ingredients: The ingredients of this Recipe.
        :type ingredients: List[str]
        """

        self._ingredients = ingredients

    @property
    def instructions(self):
        """Gets the instructions of this Recipe.


        :return: The instructions of this Recipe.
        :rtype: str
        """
        return self._instructions

    @instructions.setter
    def instructions(self, instructions):
        """Sets the instructions of this Recipe.


        :param instructions: The instructions of this Recipe.
        :type instructions: str
        """

        self._instructions = instructions

    @property
    def created_at(self):
        """Gets the created_at of this Recipe.


        :return: The created_at of this Recipe.
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this Recipe.


        :param created_at: The created_at of this Recipe.
        :type created_at: datetime
        """

        self._created_at = created_at