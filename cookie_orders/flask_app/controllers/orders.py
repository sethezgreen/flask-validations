from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import order # import entire file, rather than class, to avoid circular imports
# As you add model files add them the the import above
# This file is the second stop in Flask's thought process, here it looks for a route that matches the request

# Create Orders Controller

@app.route('/cookies/new', methods=["GET", "POST"])
def create_cookie():
    if request.method == "GET":
        return render_template('/new_cookie.html')
    if order.Order.create(request.form):
        return redirect ('/')
    return redirect ('/cookies/new')

# Read Orders Controller

@app.route('/')
def index():
    return redirect('/cookies')

@app.route('/cookies')
def cookies():
    all_orders = order.Order.get_all_orders()
    return render_template('cookies.html', all_orders = all_orders)


# Update Orders Controller

@app.route('/cookies/edit/<int:order_id>')
def update_order_form(order_id):
    one_order = order.Order.get_order_by_id(order_id)
    return render_template('edit_cookie.html', order = one_order)

@app.route('/cookies/update', methods=["POST"])
def update_order():
    if order.Order.update_order(request.form):
        return redirect ('/')
    return redirect(f"/cookies/edit/{request.form['id']}")

# Delete Orders Controller

@app.route('/cookies/delete/<int:order_id>')
def delete_order(order_id):
    order.Order.delete(order_id)
    return redirect ('/')

# Notes:
# 1 - Use meaningful names
# 2 - Do not overwrite function names
# 3 - No matchy, no worky
# 4 - Use consistent naming conventions 
# 5 - Keep it clean
# 6 - Test every little line before progressing
# 7 - READ ERROR MESSAGES!!!!!!
# 8 - Error messages are found in the browser and terminal




# How to use path variables:
# @app.route('/<int:id>')                                   The variable must be in the path within angle brackets
# def index(id):                                            It must also be passed into the function as an argument/parameter
#     user_info = user.User.get_user_by_id(id)              The it will be able to be used within the function for that route
#     return render_template('index.html', user_info)

# Converter -	Description
# string -	Accepts any text without a slash (the default).
# int -	Accepts integers.
# float -	Like int but for floating point values.
# path 	-Like string but accepts slashes.

# Render template is a function that takes in a template name in the form of a string, then any number of named arguments containing data to pass to that template where it will be integrated via the use of jinja
# Redirect redirects from one route to another, this should always be done following a form submission. Don't render on a form submission.