
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
# import re
# from flask_bcrypt import Bcrypt
# bcrypt = Bcrypt(app)
# The above is used when we do login registration, flask-bcrypt should already be in your env check the pipfile

# Remember 'fat models, skinny controllers' more logic should go in here rather than in your controller. Your controller should be able to just call a function from the model for what it needs, ideally.

class Order:
    db = "cookie_orders_schema" #which database are you using for this project
    def __init__(self, data):
        self.id = data['id']
        self.customer_name = data['customer_name']
        self.cookie_type = data['cookie_type']
        self.num_of_boxes = data['num_of_boxes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # What changes need to be made above for this project?
        #What needs to be added here for class association?



    # Create Orders Models

    @classmethod
    def create(cls, data):
        if not cls.validate_order(data): return False
        data = {
            'customer_name' : data['customer_name'], 
            'cookie_type' : data['cookie_type'],
            'num_of_boxes' : data['num_of_boxes'] 
        }
        query = """
            INSERT INTO orders (customer_name, cookie_type, num_of_boxes)
            VALUES (%(customer_name)s, %(cookie_type)s, %(num_of_boxes)s)
            ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        return True

    # Read Orders Models

    @classmethod
    def get_all_orders(cls):
        query = """
            SELECT * FROM orders
            ;"""
        results = connectToMySQL(cls.db).query_db(query)
        all_orders = []
        for result in results:
            one_order = {
                'id' : result['id'],
                'customer_name' : result['customer_name'],
                'cookie_type' : result['cookie_type'],
                'num_of_boxes' : result['num_of_boxes'],
                'created_at' : result['created_at'],
                'updated_at' : result['updated_at']
            }
            all_orders.append(one_order)
        return all_orders
    
    @classmethod
    def get_order_by_id(cls, order_id):
        data = {
            'id' : order_id
        }
        query = """
            SELECT * FROM orders
            WHERE id = %(id)s
            ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        one_order = cls(results[0])
        return one_order

    # Update Orders Models

    @classmethod
    def update_order(cls, data):
        if not cls.validate_order(data): return False
        data = {
            'id' : data['id'],
            'customer_name' : data['customer_name'], 
            'cookie_type' : data['cookie_type'],
            'num_of_boxes' : data['num_of_boxes']
        }
        query = """
            UPDATE orders
            SET
                customer_name = %(customer_name)s,
                cookie_type = %(cookie_type)s,
                num_of_boxes = %(num_of_boxes)s
            WHERE id = %(id)s
            ;"""
        connectToMySQL(cls.db).query_db(query, data)
        return True

    # Delete Orders Models

    @classmethod
    def delete(cls, order_id):
        data = {
            'id' : order_id
        }
        query = """
            DELETE FROM orders
            WHERE id = %(id)s
            ;"""
        connectToMySQL(cls.db).query_db(query, data)
        return True

    # Validation
    @staticmethod
    def validate_order(data):
        is_valid = True
        if len(data['customer_name']) < 1:
            flash("Name must not be blank")
            is_valid = False
        if "cookie_type" not in data:
            flash("Please select a cookie type")
            is_valid = False
        if len(data['num_of_boxes']) == 0:
            flash("Please provide the number of boxes")
            is_valid = False
        return is_valid