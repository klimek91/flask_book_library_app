from book_library_app import db
from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import datetime
from flask_sqlalchemy import BaseQuery


class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<{self.__class__.__name__}>:{self.first_name} {self.last_name}'

    @staticmethod
    def get_schema_args(fields: str) -> dict:
        schema_args = {'many':True}
        if fields:
            schema_args['only'] = [field for field in fields.split(',') if field in Author.__table__.columns]
        return schema_args

    @staticmethod
    def apply_order(query: BaseQuery, sort_keys:str) -> BaseQuery:
        if sort_keys:
            for key in sort_keys.split(','):
                descending = False
                if key.startswith(('-')):
                    key = key[1:]
                    descending = True
                column_attr = getattr(Author, key, None)
                if column_attr is not None:
                    query = query.order_by(column_attr.desc()) if descending else query.order_by(column_attr)
        return query



class AuthorSchema(Schema):
    id = fields.Integer(dump_only=True)
    first_name = fields.String(required=True, validate=validate.Length(max=50))
    last_name = fields.String(required=True, validate=validate.Length(max=50))
    birth_date = fields.Date('%d-%m-%Y', required=True)

    @validates('birth_date')
    def validate_birth_date(self, value):
        if value > datetime.now().date():
            raise ValidationError(f'Birth date must be lower then {datetime.now().date()}')

author_schema = AuthorSchema()
