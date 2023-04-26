from app.bookmarks import bookmarks
from flask import request
from validators import url
from app.constants.http_status_codes import *
from app.models import Bookmark, db
from flask import json, jsonify
from flask_login import current_user

@bookmarks.route('/')
def register():
    return "Success"

@bookmarks.route('/',methods=['POST','GET'])
def handle_bookmark():
    if request.method == 'POST':
        body = request.get_json('body','')
        url = request.get_json('url','')

    if not url(url):
        return ({

            "error":"Enter a valid URL."
        }), HTTP_400_BAD_REQUEST
    
    if Bookmark.query.filter_by(url=url):
        return json({
            "error":"The URL already exists."
        })

    bookmark = Bookmark(url=url, body=body, user_id=current_user.id)
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