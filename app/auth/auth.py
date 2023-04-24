from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.constants.http_status_codes import *
import validators
from app.models import User, db
from app.auth import auth


@auth.route('/register')
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['username']
    password_hash = generate_password_hash(password)


    if len(password)<6:
        return jsonify({'error':'The password entered was too short.'}), HTTP_400_BAD_REQUEST
    
    if username.isalnum() or ' ' in username:
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