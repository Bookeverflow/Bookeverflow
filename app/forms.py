from wtforms import (
    BooleanField, StringField, IntegerField, FileField, TextAreaField, validators)
from flask_wtf import FlaskForm


class AddBookForm(FlaskForm):
    name = StringField('Book name', [validators.DataRequired()])
    author = StringField('Author')
    book_type = StringField('Book type', [validators.DataRequired()])
    description = TextAreaField('Short description', [validators.DataRequired()])
    language = StringField('Book language')
    image = FileField('Upload a book image')
    price = IntegerField('Rent price')
    target_place = StringField('Available location')
