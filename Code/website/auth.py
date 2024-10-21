
from datetime import timedelta
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt
from werkzeug.security import generate_password_hash
from . import db
from .models import User

auth = Blueprint('auth', __name__)

blacklist = set()


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    print(email, password)
    user = User.query.filter_by(email=email).first()
    if user and user.check_pass(password):
        access_token = create_access_token(
            identity={'email': user.email, 'role': user.role}, expires_delta=timedelta(days=1))
        response = make_response({'message': "Login Successful"})
        response.set_cookie('access_token', access_token,
                            secure=True, max_age=99999)
        return response
    return jsonify({"error": "Invalid credentials"}), 401


@auth.route('logout', methods=['GET'])
@jwt_required()
def logout():
    response = make_response({"message": "Logout Successful"})
    response.delete_cookie('access_token')
    response.status_code = 200
    return response


@auth.route('/register', methods=['GET', 'POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'user')  # Default to 'user' role if not provided
    xp = data.get('xp', {})  # Default to empty XP data if not provided

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 400

    new_user = User(
        email=email, password=generate_password_hash(password), role=role, xp=xp)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201


@auth.route("getuser", methods=["GET"])
@jwt_required(optional=True)
def getuser():
    curr_user = get_jwt_identity()
    if (curr_user == None):
        return jsonify({"error": "user not logged in"}), 400
    return jsonify({"email": curr_user["email"], "role": curr_user["role"]})


@auth.route("token", methods=["GET"])
def generateToken():
    return jsonify({"access_token": create_access_token({"email": "guest@store.com", "role": "guest"})}), 200
