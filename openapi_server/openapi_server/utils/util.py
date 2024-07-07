from flask_jwt_extended import verify_jwt_in_request, get_jwt,get_jwt_identity
from functools import wraps
from flask import jsonify

from openapi_server.models.db_schema import Recipe
def role_required(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Verify JWT in the request headers
            verify_jwt_in_request()

            # Retrieve JWT claims
            claims = get_jwt()

            # Check if 'role' claim exists and matches the required role
            if 'role' not in claims:
                return jsonify(message='Missing role claim in JWT'), 403
            if claims['role'] != role:
                return jsonify(message=f'Insufficient permissions. Required role: {role}'), 403

            # Proceed with the wrapped function
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def check_user_permissions(recipe):
    current_user_id = get_jwt_identity()
    jwt_claims = get_jwt()
    user_role = jwt_claims.get('role', '')

    if current_user_id == recipe.author_id or user_role == 'admin':
        return True
    return False

def permission_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        recipe = Recipe.query.get(kwargs['recipe_id'])
        if not recipe:
            return jsonify({'error': 'Recipe not found'}), 404
        
        if not check_user_permissions(recipe):
            return jsonify({'error': 'Permission denied'}), 403
        
        return f(*args, **kwargs)
    return decorator
