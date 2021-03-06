from webargs.flaskparser import use_args
from flask import abort, jsonify

from book_library_app import db
from book_library_app.auth import auth_bp
from book_library_app.models import user_schema, User
from book_library_app.utils import validate_json_content_type


@auth_bp.route('/register', methods=['POST'])
@validate_json_content_type
@use_args(user_schema, error_status_code=400)
def register(args: dict):
    if User.query.filter(User.username == args['username']).first():
        abort(409, description = f'User with username {args["username"]} already exists')
    if User.query.filter(User.email == args['email']).first():
        abort(409, description = f'User with email {args["email"]} already exists')

    args['password'] = User.generate_hashed_password(args['password'])
    user = User(**args)

    db.session.add(user)
    db.session.commit()

    token = user.generate_jwt()

    return jsonify({
        'success':True,
        'token': token.decode()
    })