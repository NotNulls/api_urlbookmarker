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
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 5, type=int)

            bookmks= Bookmark.query.filter_by(user_id=current_user.id).paginate(page=page, per_page=per_page)

            data=[]

            for bkmk in bookmks.items:
                data.append({
                    'id':bkmk.id,
                    'url':bkmk.url,
                    'short_url':bkmk.short_url,
                    'visits':bkmk.visits,
                    'created_at':bkmk.created,
                    'updated_at':bkmk.created,
                })

            meta = {
                "page":bookmks.pages,
                "pages":bookmks.pages,
                "total_""pages":bookmks.total,
                "prev_page":bookmks.prev_num,
                "next_page":bookmks.next_num,
                "has_next":bookmks.has_next,
                "has_prev":bookmks.has_prev,
            }

    return jsonify({'data':data, "meta":meta})

@bookmarks.route("/<int:id>")
@jwt_required()
def get_bookmark(id):
    if current_user.is_authenticated:

        bookmark = Bookmark.query.filter_by(user_id=current_user.id, id=id).first()

        if not bookmark:
            return jsonify({"message":"Item not found"}), HTTP_404_NOT_FOUND
        
    return jsonify({
                    'id':bookmark.id,
                    'url':bookmark.url,
                    'short_url':bookmark.short_url,
                    'visits':bookmark.visits,
                    'body':bookmark.body,
                    'created_at':bookmark.created,
                    'updated_at':bookmark.created,
                })
            

@bookmarks.put('/<int:id>')
@bookmarks.patch('/<int:id>')
@login_required
@jwt_required()
def edit_bookmark(id):
    if current_user.is_authenticated:

        bookmark = Bookmark.query.filter_by(user_id=current_user.id, id=id).first()
        
        if not bookmark:
            return jsonify({"message":"Item not found"}), HTTP_404_NOT_FOUND
        
        body = request.get_json().get('body', '')
        url = request.get_json().get('url', '')

        if not validators.url(url):
                return ({
                    "error":"Enter a valid URL."
                }), HTTP_400_BAD_REQUEST
        
        bookmark.url = url
        bookmark.body = body

        db.session.commit()

        return jsonify({'user': {
                    'id':bookmark.id,
                    'url':bookmark.url,
                    'short_url':bookmark.short_url,
                    'visits':bookmark.visits,
                    'body':bookmark.body,
                    'created_at':bookmark.created,
                    'updated_at':bookmark.created,
                }}),HTTP_200_OK
    
@bookmarks.route('/<int:id>', methods = ["DELETE"])
@jwt_required()
def delete(id):
    if current_user.is_authenticated:
        if request.method == "DELETE":

            bookmark = Bookmark.query.filter_by(user_id=current_user.id, id=id).first()

            if not bookmark:
                return ({
                    "error":"Enter a valid URL."
                }), HTTP_400_BAD_REQUEST
            
            db.session.delete(bookmark)
            db.session.commit()

            return jsonify({}), HTTP_204_NO_CONTENT