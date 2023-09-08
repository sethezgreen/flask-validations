from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = "users_schema"
    def __init__(self, data) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

# CREATE: class method for creating users in our database
    @classmethod
    def save_new_user(cls, data):
        query = """INSERT INTO users (first_name, last_name, email, created_at, updated_at)
                    VALUES (%(first_name)s, %(last_name)s, %(email)s, NOW(), NOW());"""
        return connectToMySQL(cls.db).query_db(query, data)

# READ: class method for selecting all users from the db
    @classmethod
    def get_all_users(cls):
        # query for selecting all from users table in mysql
        query = "SELECT * FROM users;"
        # calling the connectToMySQL function with the users_schema
        results = connectToMySQL(cls.db).query_db(query)
        # creating an empty list to append instances of users
        users = []
        # iterate over the db results and create instances of users with cls
        for user in results:
            users.append(cls(user))
        return users
    
# READ: class method for selecting one user
    @classmethod
    def get_user_by_id(cls, user_id):
        query = """SELECT * FROM users 
                    WHERE id = %(user_id)s;"""
        results = connectToMySQL(cls.db).query_db(query, {"user_id": user_id} )
        return cls(results[0])

    
    
# UPDATE: class method for updating one user
    @classmethod
    def update_user(cls, data):
        query = "UPDATE users SET first_name=%(first_name)s,last_name=%(last_name)s,email=%(email)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    
# DELETE: class method for deleting one user
    @classmethod
    def delete_user_by_id(cls, user_id):
        query = """DELETE FROM users 
                    WHERE id = %(id)s;"""
        data = {"id": user_id}
        return connectToMySQL(cls.db).query_db(query,data)

# VALIDATION
    @staticmethod
    def validate_user(user):
        is_vaild = True
        if len(user['first_name']) < 1:
            flash("First Name is required")
            is_vaild = False
        if len(user['last_name']) < 1:
            flash("Last Name is required")
            is_vaild = False
        if len(user['email']) < 1:
            flash("Email is required")
            is_vaild = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email")
            is_vaild = False
        return is_vaild