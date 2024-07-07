import connexion
import six
from flask import jsonify
from openapi_server.models.inline_object import InlineObject  # noqa: E501
from openapi_server.models.inline_object1 import InlineObject1  # noqa: E501
from openapi_server.models.inline_object2 import InlineObject2  # noqa: E501
from openapi_server.models.inline_object3 import InlineObject3  # noqa: E501
from openapi_server.models.inline_object4 import InlineObject4 
from openapi_server.models.inline_object5 import InlineObject5 # noqa: E501
from openapi_server.models.inline_response200 import InlineResponse200  # noqa: E501
from openapi_server.models.inline_response201 import InlineResponse201  # noqa: E501
from openapi_server import util
from openapi_server.models.db_schema import Like, db, Recipe,Comment,User
from datetime import datetime,timedelta
from flask_jwt_extended import jwt_required,create_access_token
from openapi_server.utils.util import role_required,permission_required
from werkzeug.security import generate_password_hash, check_password_hash


def login_post():  # noqa: E501
    """Obtain JWT token by logging in

     # noqa: E501

    :param inline_object4: 
    :type inline_object4: dict | bytes

    :rtype: InlineResponse2003
    """
    if connexion.request.is_json:
        inline_object5 = InlineObject5.from_dict(connexion.request.get_json())  # noqa: E501
    username = inline_object5.username
    password = inline_object5.password
    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password_hash,password):
        return jsonify({"message": "Invalid username or password"}), 401

    # Create JWT token
    expires = timedelta(minutes=15)
    access_token = create_access_token(identity=user.id, additional_claims={"role": user.role},expires_delta=expires)

    return jsonify(access_token=access_token), 200

@jwt_required()
def recipes_recipe_id_likes_get(recipe_id):  # noqa: E501
    """Get likes for a recipe

     # noqa: E501

    :param recipe_id: 
    :type recipe_id: int

    :rtype: List[InlineResponse2001]
    """
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404

    # Query likes for the valid recipe
    likes = Like.query.filter_by(recipe_id=recipe_id).all()
    if not likes:
        return jsonify({'error': 'No likes found for this recipe'}), 404

    user_ids = [like.user_id for like in likes]
    return jsonify(user_ids), 200


@jwt_required()
def recipes_recipe_id_comments_get(recipe_id):  # noqa: E501
    """Get comments for a recipe

     # noqa: E501

    :param recipe_id: 
    :type recipe_id: int

    :rtype: List[InlineResponse2002]
    """
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404
    comments = Comment.query.filter_by(recipe_id=recipe_id).all()
    comments_list = [comment.as_dict() for comment in comments]
    return jsonify(comments_list)

@jwt_required()
def recipes_get(page=None, per_page=None):  # noqa: E501
    """Get all recipes with pagination

     # noqa: E501

    :param page: 
    :type page: int
    :param per_page: 
    :type per_page: int

    :rtype: InlineResponse200
    """
    if page is None:
        page = 1
    if per_page is None:
        per_page = 10
    """
    SELECT * FROM table_name
    OFFSET (page - 1) * per_page
    LIMIT per_page;

    """
    pagination = Recipe.query.paginate(page=page, per_page=per_page, error_out=False)
    
    recipes = pagination.items
    total = pagination.total
    pages = pagination.pages
    
    data = [recipe.as_dict() for recipe in recipes]
    
    return jsonify({
        'total': total,
        'pages': pages,
        'current_page': page,
        'per_page': per_page,
        'data': data
    }), 200 
    
@jwt_required()
def recipes_post():  # noqa: E501
    """Create a new recipe

     # noqa: E501

    :param inline_object: 
    :type inline_object: dict | bytes

    :rtype: Recipe
    """
    if connexion.request.is_json:
        inline_object = InlineObject.from_dict(connexion.request.get_json())  # noqa: E501
    
    # Extract data from JSON request
    author_id = inline_object.author_id
    title  = inline_object.title
    description = inline_object.description
    ingredients = inline_object.ingredients
    instructions = inline_object.instructions
    
    # Create new Recipe object

    new_recipe = Recipe(
        author_id=author_id,
        title=title,
        description=description,
        ingredients=ingredients,
        instructions=instructions,
        created_at=datetime.utcnow()  # Use UTC time for consistency
    )
    
    # Add to session and commit to database
    db.session.add(new_recipe)
    db.session.commit()
    
    return jsonify({'message': 'Recipe created successfully', 'recipe_id': new_recipe.id}), 201

@jwt_required()
def recipes_recipe_id_comments_post(recipe_id):  # noqa: E501
    """Add a comment to a recipe

     # noqa: E501

    :param recipe_id: 
    :type recipe_id: int
    :param inline_object3: 
    :type inline_object3: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        inline_object3 = InlineObject3.from_dict(connexion.request.get_json())  # noqa: E501
    
    user_id = inline_object3.user_id
    text = inline_object3.text
    if not user_id or not text:
        return jsonify({'error': 'User ID and text are required'}), 400

    recipe = Recipe.query.get(recipe_id)
    if recipe is None:
        return jsonify({'error': 'Recipe not found'}), 404

    comment = Comment(recipe_id=recipe_id, user_id=user_id, text=text)
    db.session.add(comment)
    db.session.commit()

    return jsonify({'message': 'Comment added successfully'}), 201


@jwt_required()
@permission_required
def recipes_recipe_id_delete(recipe_id):  # noqa: E501
    """Delete a recipe

     # noqa: E501

    :param recipe_id: 
    :type recipe_id: int

    :rtype: None
    """
    recipe = Recipe.query.get(recipe_id)
    if recipe is None:
        return jsonify({'error': 'Recipe not found'}), 404

    db.session.delete(recipe)
    db.session.commit()

    return jsonify({'message': 'Recipe deleted successfully'}), 202

@jwt_required()
def recipes_recipe_id_get(recipe_id):  # noqa: E501
    """Fetch a recipe by ID

     # noqa: E501

    :param recipe_id: 
    :type recipe_id: int

    :rtype: Recipe
    """
    recipe = Recipe.query.get(recipe_id)
    if recipe is None:
        return jsonify({'error': 'Recipe not found'}), 404

    recipe_data = {
        'id': recipe.id,
        'author_id': recipe.author_id,
        'title': recipe.title,
        'description': recipe.description,
        'ingredients': recipe.ingredients,
        'instructions': recipe.instructions,
        'created_at': recipe.created_at.isoformat()  # Convert to ISO 8601 string
    }
    return jsonify(recipe_data), 200


@jwt_required()
def recipes_recipe_id_likes_post(recipe_id):  # noqa: E501
    """Like a recipe

     # noqa: E501

    :param recipe_id: 
    :type recipe_id: int
    :param inline_object2: 
    :type inline_object2: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        inline_object2 = InlineObject2.from_dict(connexion.request.get_json())  # noqa: E501
    user_id = inline_object2.user_id

    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    recipe = Recipe.query.get(recipe_id)
    if recipe is None:
        return jsonify({'error': 'Recipe not found'}), 404

    # Check if the user has already liked the recipe
    existing_like = Like.query.filter_by(recipe_id=recipe_id, user_id=user_id).first()
    if existing_like:
        return jsonify({'message': 'Recipe already liked'}), 400

    like = Like(recipe_id=recipe_id, user_id=user_id)
    db.session.add(like)
    db.session.commit()

    return jsonify({'message': 'Recipe liked successfully'}), 201

@jwt_required()
@permission_required
def recipes_recipe_id_put(recipe_id):  # noqa: E501
    """Update an existing recipe

     # noqa: E501

    :param recipe_id: 
    :type recipe_id: int
    :param inline_object1: 
    :type inline_object1: dict | bytes

    :rtype: Recipe
    """
    if connexion.request.is_json:
        inline_object1 = InlineObject1.from_dict(connexion.request.get_json())  # noqa: E501
    recipe = Recipe.query.get(recipe_id)
    if recipe is None:
        return jsonify({'error': 'Recipe not found'}), 404


    if not inline_object1:
        return jsonify({'error': 'Invalid request payload'}), 400

    title = inline_object1.title
    description = inline_object1.description
    ingredients = inline_object1.ingredients
    instructions = inline_object1.instructions

    if title:
        recipe.title = title
    if description:
        recipe.description = description
    if ingredients:
        recipe.ingredients = ingredients
    if instructions:
        recipe.instructions = instructions

    db.session.commit()

    return jsonify({
        'message': 'Recipe updated successfully',
        'recipe': {
            'id': recipe.id,
            'author_id': recipe.author_id,
            'title': recipe.title,
            'description': recipe.description,
            'ingredients': recipe.ingredients,
            'instructions': recipe.instructions,
            'created_at': recipe.created_at.isoformat()  # Convert to ISO 8601 string
        }
    }), 200


@role_required('admin')
def users_post():  # noqa: E501
    """Create a new user (admin only)

     # noqa: E501

    :param inline_object4: 
    :type inline_object4: dict | bytes

    :rtype: InlineResponse201
    """
    if connexion.request.is_json:
        inline_object4 = InlineObject4.from_dict(connexion.request.get_json())  # noqa: E501
    username = inline_object4.username 
    password =  inline_object4.password
    role  = inline_object4.role

    if not username or not password or not role:
        return jsonify({'error': 'Missing username or password'}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 400
    new_user = User()
    new_user.username = username
    new_user.password_hash = generate_password_hash(password)
    new_user.role = role
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': f'User created successfully with id {new_user.id}'}), 201

@role_required('admin')
def users_user_id_delete(user_name):  # noqa: E501
    """Delete a user (admin only)

     # noqa: E501

    :param user_id: 
    :type user_id: int

    :rtype: None
    """
    user = User.query.filter_by(username=user_name).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify(), 204
