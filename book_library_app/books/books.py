from flask import jsonify

from book_library_app.models import Book, BookSchema, book_schema
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

@books_bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id: int):
    book = Book.query.get_or_404(book_id, description=f"Author with id {book_id} not found!")
    return jsonify({
        'success':True,
        'data': book_schema.dump(book),
    })
