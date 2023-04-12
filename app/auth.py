from flask import Blueprint

auth = Blueprint('auth',__name__,url_prefix='/api/v1/auth')

@auth.route('/register')
def register():
    return "Success"