import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_openid import OpenID
from config import basedir
from flask_oauth import OAuth


app = Flask(__name__, static_url_path='/static')
app.config.from_object('config')

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key='695100813997374',
    consumer_secret='ee73782e44fd97dea15305d6fb7ef9a8',
    request_token_params={'scope': 'email'}
)


from app import views, models
