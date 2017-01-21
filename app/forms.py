from wtforms import (
    BooleanField, StringField, IntegerField, FileField, validators)
from flask_wtf import FlaskForm


class AddBookForm(FlaskForm):
    name = StringField('Book name', [validators.DataRequired()])
    author = StringField('Author')
    book_type = StringField('Book type', [validators.DataRequired()])
    description = StringField('Short description', [validators.DataRequired()])
    language = StringField('Book language')
    image = FileField('Upload a book image')
    price = IntegerField('Rent price')
    service_type = IntegerField('Target Service:')
    target_place = StringField('Available location')
