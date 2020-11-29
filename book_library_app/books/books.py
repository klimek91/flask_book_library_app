from flask import jsonify

from book_library_app.models import Book, BookSchema
from book_library_app.utils import get_schema_args, apply_order, apply_filter, get_pagination, validate_json_content_type
from book_library_app.books import books_bp



@books_bp.route('/books', methods=['GET'])
def get_books():
    query = Book.query
    schema_args = get_schema_args(Book)
    query = apply_order(Book, query)
    query = apply_filter(Book, query)
    items, pagination = get_pagination(query, 'books.get_books')

    books = BookSchema(**schema_args).dump(items)

    return jsonify({
        'success':True,
        'data': books,
        'number_of_redords': len(books),
        'pagination' : pagination
    })