import json
from flask import Blueprint, jsonify, session, request
from app.models import User, db
from app.forms import LoginForm
from app.forms import SignUpForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import ShoppingCartItem

auth_routes = Blueprint('auth', __name__)


def validation_errors_to_error_messages(validation_errors):
    """
    Simple function that turns the WTForms validation errors into a simple list
    """
    errorMessages = []
    for field in validation_errors:
        for error in validation_errors[field]:
            errorMessages.append(f'{field} : {error}')
    return errorMessages


@auth_routes.route('/')
def authenticate():
    """
    Authenticates a user
    """
    if current_user.is_authenticated:
        return current_user.to_dict()
    return {'errors': ['Unauthorized']}


@auth_routes.route('/login', methods=['POST'])
def login():
    """
    Logs a user in
    """
    form = LoginForm()
    # Get the csrf_token from the request cookie and put it into the
    # form manually to validate_on_submit can be used
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
    # Add the user to the session, we are logged in!
        user = User.query.filter(User.email == form.data['email']).first()
        shopping_cart = ShoppingCartItem.query.filter_by(user_id=user.id).all()
        cart_res = [{column.name: getattr(cart_item, column.name) for column in cart_item.__table__.columns} for cart_item in shopping_cart]

        login_user(user)

        user_data = user.to_dict()  # Convert user to dict
        user_data['shopping_cart'] = cart_res  # Add shopping cart to user data

        return {'User': user_data}
    return {'errors': validation_errors_to_error_messages(form.errors)}, 401








@auth_routes.route('/logout')
def logout():
    """
    Logs a user out
    """
    logout_user()
    return {'message': 'User logged out'}


@auth_routes.route('/signup', methods=['POST'])
def sign_up():
    """
    Creates a new user and logs them in
    """
    form = SignUpForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        user = User(
            username=form.data['username'],
            email=form.data['email'],
            password=form.data['password']
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
<<<<<<< HEAD
        return json.dumps([{'User': user.to_dict()}, {'Shopping cart': []}])
=======
        return {'User': user.to_dict(), 'Shopping cart': []}
>>>>>>> remotes/origin/dev
    return {'errors': validation_errors_to_error_messages(form.errors)}, 401


@auth_routes.route('/unauthorized')
def unauthorized():
    """
    Returns unauthorized JSON when flask-login authentication fails
    """
    return {'errors': ['Unauthorized']}, 401
