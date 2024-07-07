#!/usr/bin/env python3

import connexion
import os
from openapi_server import encoder
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash


db = SQLAlchemy()
app = connexion.App(__name__, specification_dir='./openapi/')
app.add_api('openapi.yaml',
                arguments={'title': 'TasteBuds API'},
                pythonic_params=True)

app.app.json_encoder = encoder.JSONEncoder
flask_app = app.app

flask_app.config['JWT_SECRET_KEY'] = 'akamai-test' 
jwt = JWTManager(flask_app)
# Configuration for the database
flask_app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@db:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
# track modifications. to avoid generate event 
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(flask_app)

# whole application context
with flask_app.app_context():
    from openapi_server.models.db_schema import User, Recipe, Like, Comment
    db.create_all()  # Create database tables for all models
    admin_user = User.query.filter_by(username='admin').first()
    # Default user admin creation 
    if not admin_user:
        admin_user = User(
            username='admin',
            password_hash=generate_password_hash('admin'),
            role='admin'
        )
        db.session.add(admin_user)
        db.session.commit()
if __name__ == '__main__':
    app.run()
