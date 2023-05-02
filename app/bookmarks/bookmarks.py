from app.bookmarks import bookmarks
from flask import request
import validators
from app.constants.http_status_codes import *
from app.models import Bookmark, db
from flask import jsonify
from flask_login import current_user, login_required
from flask_jwt_extended import jwt_required

@bookmarks.route('/register')
def register():
    return "Success"

@bookmarks.route('/',methods=['POST','GET'])
@jwt_required()
@login_required
def handle_bookmark():
    if current_user.is_authenticated:    
        if request.method == 'POST':
            
            body = request.get_json().get('body', '')
            url = request.get_json().get('url', '')

            if not validators.url(url):
                return ({
                    "error":"Enter a valid URL."
                }), HTTP_400_BAD_REQUEST
            
            if Bookmark.query.filter_by(url=url).first():
                return jsonify({
                    "error":"The URL already exists."
                })

            bookmark = Bookmark(body=body, url=url, user_id=current_user.id,)
            db.session.add(bookmark)
            db.session.commit()

            return jsonify({
                'user': {
                    'id':bookmark.id,
                    'url':bookmark.url,
                    'short_url':bookmark.short_url,
                    'visits':bookmark.visits,
                    'created_at':bookmark.created,
                    'updated_at':bookmark.created,
                }
            }), HTTP_200_OK

        else:
            bookmks= Bookmark.query.filter_by(user_id=current_user.id)

            data=[]

            for bkmk in bookmks:
                data.append({
                    'id':bookmark.id,
                    'url':bookmark.url,
                    'short_url':bookmark.short_url,
                    'visits':bookmark.visits,
                    'created_at':bookmark.created,
                    'updated_at':bookmark.created,
                })

            return jsonify({'data':data})
        