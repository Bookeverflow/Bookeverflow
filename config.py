import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

WTF_CSRF_ENABLED = True
SECRET_KEY = 'ASd312da09093Cfnafk'

OAUTH_CREDENTIALS = {
    'facebook': {
        'id': '695100813997374',
        'secret': 'ee73782e44fd97dea15305d6fb7ef9a8'
    },
}
