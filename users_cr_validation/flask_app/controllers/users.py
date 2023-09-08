from flask_app import app
from flask import Flask, redirect, render_template, request, session, url_for
from flask_app.models import user

# Create users controller
@app.route('/users/create', methods=["POST"])
def create_user():
    # data for prepared statement
    if not user.User.validate_user(request.form):
        return redirect('/users/new')
    else:
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email']
        }
        # pass in the data dict using the method from User
        new_user_id = user.User.save_new_user(data)
        # return redirect(url_for('read_one_user', user_id = new_user_id))
        return redirect(f'/users/{new_user_id}')

@app.route('/')
def index():
    return redirect('/users')

# Read users controllers
@app.route('/users')
def read_all_users():
    users = user.User.get_all_users()
    print(users)
    return render_template('read_all.html', users = users)

# Read one user
@app.route('/users/<int:user_id>')
def read_one_user(user_id):
    one_user = user.User.get_user_by_id(user_id)
    return render_template("read_one.html", one_user = one_user)

# Create route to create.html
@app.route('/users/new')
def create_user_page():
    return render_template('create.html')

# Update controllers
@app.route('/users/<int:user_id>/edit')
def edit_user_page(user_id):
    one_user = user.User.get_user_by_id(user_id)
    return render_template("edit.html", one_user = one_user)

@app.route('/users/update', methods=["POST"])
def update_user():
    if not user.User.validate_user(request.form):
        return redirect('/')
    else:
        user.User.update_user(request.form)
        return redirect(url_for('read_one_user', user_id = request.form['id']))

# Delete controller
@app.route("/users/delete/<int:user_id>")
def delete_user(user_id):
    user.User.delete_user_by_id(user_id)
    return redirect('/users')