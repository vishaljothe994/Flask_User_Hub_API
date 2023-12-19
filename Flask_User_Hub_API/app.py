from flask import Flask, jsonify, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from datetime import timedelta
import jwt  
from datetime import datetime, timedelta
from flask import request
from secrets import token_urlsafe 
from flask_mail import Mail, Message
from flask_swagger_ui import get_swaggerui_blueprint


app = Flask(__name__)


# Define the Swagger UI blueprint
SWAGGER_URL = '/swagger'  # URL for accessing Swagger UI
API_URL = '/static/swagger.json'  # URL to your API documentation

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Flask Swagger Demo"
    }
)

app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


# Initialize Flask-Mail
app.config['MAIL_SERVER'] = '**********'  # Your SMTP server
app.config['MAIL_PORT'] = ********** # Your SMTP server's port (587 for TLS)
app.config['MAIL_USE_TLS'] = True  # Use TLS (True for TLS, False for SSL)
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = '**********'  # Your email username
app.config['MAIL_PASSWORD'] = '**********'  # Your email password
app.config['MAIL_DEFAULT_SENDER'] = 'Desired Name <**********>'  # Your default sender email
mail = Mail(app)

app.config['SECRET_KEY'] = 'SECRET_KEY'

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
CORS(app)


# Configure your database connection URL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://***username***:***password***@localhost/***databasename***'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    username = None
    isPaid = db.Column(db.Boolean, default=False)
    TrialsLeft = db.Column(db.Integer, default=20)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, onupdate=datetime.utcnow)

class UserToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create the database tables within an application context
with app.app_context():
    db.create_all()


# User Registration
@app.route('/register', methods=['POST'])
def register():
    """
    User registration endpoint.
    """
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    # Check if the email already exists
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"message": "Email already registered"}), 400

    # Create a new user
    new_user = User(name=name, email=email, password=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Registration successful"})


# User Login
@app.route('/login', methods=['POST'])
def login():
    """
    User login endpoint.
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        
        # Generate a JWT token with the user's email and an expiration time
        expiration_time = datetime.utcnow() + timedelta(minutes=2)  # You can adjust the expiration time as needed
        token_payload = {'email': email, 'exp': expiration_time}
        jwt_token = jwt.encode(token_payload, app.config['SECRET_KEY'], algorithm='HS256')

        # Include the JWT token in the login response
        response_data = {
            "message": "Login successful",
            "token": jwt_token  # Include the token in the response
        }
        return jsonify(response_data)

    return jsonify({"message": "Invalid credentials"}), 401


# User Profile View
@app.route('/user/<int:user_id>', methods=['GET'])
def user_profile_view(user_id):
    """
    User profile view endpoint.
    """

    # Check if the user is authenticated with a valid JWT token
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"message": "Authorization token is missing"}), 401

    try:
        # Verify and decode the JWT token
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 401

    # Check if the user ID in the URL matches the authenticated user's email
    authenticated_user_email = payload['email']

    qry_user = User.query.filter_by(email=authenticated_user_email).first()
    print("qry_user" , qry_user)

    # qry_user = User.query.get(id=user_id)
    if not qry_user:
        return jsonify({"message": "User not found"}), 404

    if authenticated_user_email != qry_user.email:
        return jsonify({"message": "Access denied"}), 403

    # Replace this with your own logic to retrieve user profile data
    user_profile_data = {
        "user_id": qry_user.id,
        "name": qry_user.name,
        "email": qry_user.email,
        "password": qry_user.password,
        "isPaid": qry_user.isPaid,
        "TrialsLeft": qry_user.TrialsLeft,
        "createdAt": qry_user.createdAt.strftime('%Y-%m-%d %H:%M:%S'),
        "updatedAt": qry_user.updatedAt.strftime('%Y-%m-%d %H:%M:%S') if qry_user.updatedAt else None
        # Include other profile data as needed
    }

    return jsonify(user_profile_data)


# Update User Profile
@app.route('/updateuser/<int:user_id>', methods=['PUT'])
def update_user_profile(user_id):
    """
    Update user profile endpoint.
    """

    # Check if the user is authenticated with a valid JWT token
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"message": "Authorization token is missing"}), 401 

    try:
        # Verify and decode the JWT token
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 401

    # Check if the user email in the JWT payload matches the requested user's email
    authenticated_user_email = payload['email']

    qry_user = User.query.filter_by(email=authenticated_user_email).first()

    if not qry_user:
        return jsonify({"message": "User not found"}), 404

    # Check if the email in the JWT payload matches the user's email
    if authenticated_user_email != qry_user.email:
        return jsonify({"message": "Access denied"}), 403

    # Parse the request data (e.g., JSON) to update the user's profile
    data = request.get_json()
    
    # Update the user's profile data as needed
    if 'name' in data:
        qry_user.name = data['name']
    if 'password' in data:
        qry_user.password = generate_password_hash(data['password'])
    # Add more fields as necessary

    db.session.commit()

    return jsonify({"message": "Profile updated successfully"})

# Forgot Password
@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    """
    Forgot password endpoint.
    """
    data = request.get_json()
    email = data.get('email')

    reset_token = token_urlsafe(32)
    reset_url = f"http://abc.com/reset-password?token={reset_token}"

    # Create the email message with a custom format
    msg = Message('Password Reset', recipients=[email])
    msg.html = f'''
    <p>Dear User,</p>
    <p>A forgot-password request has been received from this email ID from TummyTango.</p>
    <p>Click the following link to reset your password:</p>
    <a href="{reset_url}">Reset Password</a>
    <p>Thank You,<br>abc</p>
    '''

    # Save the reset_token and create/update UserToken record
    user = User.query.filter_by(email=email).first()
    if user:
        user_token = UserToken.query.filter_by(user_id=user.id).first()
        if user_token:
            user_token.token = reset_token
            user_token.created_at = datetime.utcnow()
        else:
            user_token = UserToken(user_id=user.id, token=reset_token)

        db.session.add(user_token)
        db.session.commit()

        mail.send(msg)
        return jsonify({"message": "Password reset email sent. Check your inbox.", "reset_url": reset_url})
    else:
        return jsonify({"error": "User not found"}, 404)


# Change Password
@app.route('/change_password', methods=['POST'])
def change_password():
    """
    Change password endpoint.
    """
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('new_password')

    # Verify the token's validity and retrieve user ID
    user_token = UserToken.query.filter_by(token=token).first()
    if user_token:
        user_id = user_token.user_id

        # Retrieve user by user_id
        user = User.query.filter_by(id=user_id).first()
        if user:
            # Hash and store the new password
            if 'new_password' in data:
                user.password = generate_password_hash(data['new_password'])

            db.session.commit()
            return jsonify({"message": "Password updated successfully"}), 200
        else:
            return jsonify({"error": "User not found"}, 404)
    else:
        return jsonify({"error": "Invalid token"}, 400)        



if __name__ == '__main__':
    app.run(debug=True)    



