# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from flask_jwt_extended import create_access_token
from openapi_server.models.inline_object import InlineObject  # noqa: E501
from openapi_server.models.inline_object1 import InlineObject1  # noqa: E501
from openapi_server.models.inline_object2 import InlineObject2  # noqa: E501
from openapi_server.models.inline_object3 import InlineObject3  # noqa: E501
from openapi_server.models.inline_object4 import InlineObject4  # noqa: E501
from openapi_server.models.inline_response200 import InlineResponse200  # noqa: E501
from openapi_server.models.inline_response201 import InlineResponse201  # noqa: E501
from openapi_server.models.recipe import Recipe  # noqa: E501
from openapi_server.models.user import User  # noqa: E501
from openapi_server.test import BaseTestCase, db


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def setUp(self):
        super().setUp()
        self.admin_user = User(username='admin', password_hash='hashed_admin', role='admin')
        self.normal_user = User(username='user', password_hash='hashed_user', role='user')
        db.session.add(self.admin_user)
        db.session.add(self.normal_user)
        db.session.commit()
        self.admin_token = create_access_token(identity=self.admin_user.id, additional_claims={"role": self.admin_user.role})
        self.user_token = create_access_token(identity=self.normal_user.id, additional_claims={"role": self.normal_user.role})

    def tearDown(self):
        db.session.query(User).delete()
        db.session.query(Recipe).delete()
        db.session.commit()
        super().tearDown()

    def test_recipes_get(self):
        """Test case for recipes_get: Get all recipes with pagination"""
        query_string = [('page', 1), ('per_page', 10)]
        headers = {'Accept': 'application/json'}
        response = self.client.open(
            '/recipes',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response, 'Response body is : ' + response.data.decode('utf-8'))

    def test_recipes_post(self):
        """Test case for recipes_post: Create a new recipe"""
        inline_object = {
            "title": "New Recipe",
            "description": "Delicious new recipe",
            "ingredients": ["ingredient1", "ingredient2"],
            "instructions": "Mix and cook"
        }
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.admin_token}'
        }
        response = self.client.open(
            '/recipes',
            method='POST',
            headers=headers,
            data=json.dumps(inline_object),
            content_type='application/json')
        self.assert200(response, 'Response body is : ' + response.data.decode('utf-8'))

    def test_recipes_recipe_id_comments_post(self):
        """Test case for recipes_recipe_id_comments_post: Add a comment to a recipe"""
        recipe = Recipe(author_id=self.normal_user.id, title='Recipe', description='Desc', ingredients=['ing'], instructions='instr')
        db.session.add(recipe)
        db.session.commit()

        inline_object3 = {"comment": "Great recipe!"}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.user_token}'
        }
        response = self.client.open(
            f'/recipes/{recipe.id}/comments',
            method='POST',
            headers=headers,
            data=json.dumps(inline_object3),
            content_type='application/json')
        self.assert200(response, 'Response body is : ' + response.data.decode('utf-8'))

    def test_recipes_recipe_id_delete(self):
        """Test case for recipes_recipe_id_delete: Delete a recipe"""
        recipe = Recipe(author_id=self.normal_user.id, title='Recipe', description='Desc', ingredients=['ing'], instructions='instr')
        db.session.add(recipe)
        db.session.commit()

        headers = {'Authorization': f'Bearer {self.admin_token}'}
        response = self.client.open(
            f'/recipes/{recipe.id}',
            method='DELETE',
            headers=headers)
        self.assert200(response, 'Response body is : ' + response.data.decode('utf-8'))

    def test_recipes_recipe_id_get(self):
        """Test case for recipes_recipe_id_get: Fetch a recipe by ID"""
        recipe = Recipe(author_id=self.normal_user.id, title='Recipe', description='Desc', ingredients=['ing'], instructions='instr')
        db.session.add(recipe)
        db.session.commit()

        headers = {'Accept': 'application/json'}
        response = self.client.open(
            f'/recipes/{recipe.id}',
            method='GET',
            headers=headers)
        self.assert200(response, 'Response body is : ' + response.data.decode('utf-8'))

    def test_recipes_recipe_id_likes_post(self):
        """Test case for recipes_recipe_id_likes_post: Like a recipe"""
        recipe = Recipe(author_id=self.normal_user.id, title='Recipe', description='Desc', ingredients=['ing'], instructions='instr')
        db.session.add(recipe)
        db.session.commit()

        inline_object2 = {}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.user_token}'
        }
        response = self.client.open(
            f'/recipes/{recipe.id}/likes',
            method='POST',
            headers=headers,
            data=json.dumps(inline_object2),
            content_type='application/json')
        self.assert200(response, 'Response body is : ' + response.data.decode('utf-8'))

    def test_recipes_recipe_id_put(self):
        """Test case for recipes_recipe_id_put: Update an existing recipe"""
        recipe = Recipe(author_id=self.normal_user.id, title='Recipe', description='Desc', ingredients=['ing'], instructions='instr')
        db.session.add(recipe)
        db.session.commit()

        inline_object1 = {
            "title": "Updated Recipe",
            "description": "Updated description",
            "ingredients": ["new ingredient"],
            "instructions": "new instructions"
        }
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.user_token}'
        }
        response = self.client.open(
            f'/recipes/{recipe.id}',
            method='PUT',
            headers=headers,
            data=json.dumps(inline_object1),
            content_type='application/json')
        self.assert200(response, 'Response body is : ' + response.data.decode('utf-8'))

    def test_users_post(self):
        """Test case for users_post: Create a new user (admin only)"""
        inline_object4 = {
            "username": "newuser",
            "password": "newpassword",
            "role": "user"
        }
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.admin_token}'
        }
        response = self.client.open(
            '/users',
            method='POST',
            headers=headers,
            data=json.dumps(inline_object4),
            content_type='application/json')
        self.assert200(response, 'Response body is : ' + response.data.decode('utf-8'))

    def test_users_user_id_delete(self):
        """Test case for users_user_id_delete: Delete a user (admin only)"""
        headers = {'Authorization': f'Bearer {self.admin_token}'}
        response = self.client.open(
            '/users/{user_id}'.format(user_id=self.normal_user.id),
            method='DELETE',
            headers=headers)
        self.assert200(response, 'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
