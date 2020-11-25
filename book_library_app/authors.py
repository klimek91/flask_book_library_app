from flask import jsonify, request
from book_library_app import app, db
from book_library_app.models import Author, AuthorSchema, author_schema
from webargs.flaskparser import use_args
from book_library_app.utils import validate_json_content_type


@app.route('/api/v1/authors', methods=['GET'])
def get_authors():
    authors = Author.query.all()
    author_schema = AuthorSchema(many=True)

    return jsonify({
        'success':True,
        'data': author_schema.dump(authors),
        'number_of_redords': len(authors)
    })

@app.route('/api/v1/authors/<int:author_id>', methods=['GET'])
def get_author(author_id: int):
    author = Author.query.get_or_404(author_id, description=f"Author with id {author_id} not found!")
    return jsonify({
        'success':True,
        'data': author_schema.dump(author),
    })

@app.route('/api/v1/authors', methods=['POST'])
@validate_json_content_type
@use_args(author_schema, error_status_code=400)
def create_author(args:dict):
    author = Author(**args)
    db.session.add(author)
    db.session.commit()

    return jsonify({
        'success':True,
        'data':author_schema.dump(author)
    }), 201

@app.route('/api/v1/authors/<int:author_id>', methods=['PUT'])
@validate_json_content_type
@use_args(author_schema, error_status_code=400)
def update_author(args:dict, author_id: int):
    author = Author.query.get_or_404(author_id, description=f'Author with id {author_id} not found')

    author.first_name = args["first_name"]
    author.last_name = args["last_name"]
    author.birth_date = args["birth_date"]
    db.session.commit()

    return jsonify({
        'success':True,
        'data':author_schema.dump(author)
    })

@app.route('/api/v1/authors/<int:author_id>', methods=['DELETE'])
def delete_author(author_id: int):
    return jsonify({
        'success':True,
        'data':f'Author with id {author_id} has been deleted (test message)'
    })