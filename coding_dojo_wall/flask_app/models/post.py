
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import user
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# The above is used when we do login registration, flask-bcrypt should already be in your env check the pipfile

# Remember 'fat models, skinny controllers' more logic should go in here rather than in your controller. Your controller should be able to just call a function from the model for what it needs, ideally.

class Post:
    db = "dojo_wall_schema" #which database are you using for this project
    def __init__(self, data):
        self.id = data['id']
        self.context = data['context']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None
        # What changes need to be made above for this project?
        #What needs to be added here for class association?



    # Create Posts Models

    @classmethod
    def create_post(cls, post_data):
        if not cls.validate_post(post_data):
            return False
        post_data = {
            "content" : post_data['content'],
            "user_id" : session['user_id']
        }
        query = """
            INSERT INTO posts (content, user_id)
            VALUES (%(content)s, %(user_id)s)
            ;"""
        return connectToMySQL(cls.db).query_db(query, post_data)

    # Read Posts Models

    @classmethod
    def read_posts_with_user(cls):
        query = """
            SELECT * FROM posts
            JOIN users ON users.id = posts.user_id
            ;"""
        return connectToMySQL(cls.db).query_db(query)
    
    @classmethod
    def get_user_id_of_post(cls, post_id):
        data = {
            'id' : post_id
        }
        query = """
            SELECT user_id
            FROM posts
            WHERE id = %(id)s
            ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        return result[0]['user_id']

    # Update Posts Models



    # Delete Posts Models

    @classmethod
    def delete_post(cls, post_id):
        if session['user_id'] != cls.get_user_id_of_post(post_id): # protects posts from being deleted by other users
            return False
        data = {
            "id" : post_id
        }
        query = """
            DELETE FROM posts
            WHERE id = %(id)s
            ;"""
        connectToMySQL(cls.db).query_db(query, data)
        return True

    # Validation
    @staticmethod
    def validate_post(data):
        is_valid = True
        if len(data['content']) < 1:
            flash("*Post content must not be blank")
            is_valid = False
        return is_valid
