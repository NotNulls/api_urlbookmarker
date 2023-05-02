from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.constants.http_status_codes import *
import validators
from app.models import User, db
from app.auth import auth
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_login import login_user


@auth.route('/register', methods=["POST","GET"])
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    password_hash = generate_password_hash(password)


    if len(password)<6:
        return jsonify({'error':'The password entered was too short.'}), HTTP_400_BAD_REQUEST
    
    if not username.isalnum() or ' ' in username:
        return jsonify({'error':'The username entered needs to be alphanumeric with no spaces in within.'}), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({'error':'The email eneter must be valid.'}), HTTP_400_BAD_REQUEST
    
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error':'The email eneter already exists. Please select another one.'}), HTTP_409_CONFLICT
    
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error':'The email eneter already exists. Please select another one.'}), HTTP_409_CONFLICT

    user = User(username=username, email=email, password = password_hash)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message":"User successfuly created.",
                    "user":{
                        'username':username,
                        'email':email
                    }
                    }),HTTP_201_CREATED

@auth.route('/login', methods=['POST','GET'])
def login():
    email = request.json.get('email', "")
    password = request.json.get('password', "")

    user = User.query.filter_by(email=email).first()
    login_user(user=user)

    if user:
        is_passwrod_correct = check_password_hash(user.password, password)

        if is_passwrod_correct:
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)

            return jsonify({
                'user':{
                'refresh': refresh,
                'access' : access,
                'username' : user.username,
                'email' : user.email
                }
            }),HTTP_200_OK
    
    return jsonify(
        {
            'error message': 'Wrong credentials.'
        }
    ), HTTP_401_UNAUTHORIZED

@auth.route('/me',methods=['GET'])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        'username':user.username,
        'email':user.email
    }), HTTP_200_OK

@auth.route('/token/refresh', methods=['POST','GET'])
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return jsonify({
        'access':access
    }), 200



