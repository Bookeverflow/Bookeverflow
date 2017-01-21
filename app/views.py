import base64
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm, facebook
from models import *
from forms import *


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
@app.route('/index')
def index():
    user = g.user
    bookrecords = BookRecord.query.all()
    books = [
        {
            'uuid': record.uuid,
            'image': record.get_image(),
            'name': record.name,
            'author': record.author,
            'service_type': record.service_type,
            'language': record.language
        } for record in bookrecords]
    # books = books * 10
    return render_template('index.html',
                           title='bookeverflow',
                           books=books)


@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return facebook.authorize(
        callback=url_for('facebook_authorized',
                         next=request.args.get(
                             'next') or request.referrer or None,
                         _external=True))


@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')

    user = User.query.filter_by(social_id=me.data['id']).first()
    if user is None:
        user = User()
        user.social_id = me.data['id']
    user.nickname = me.data['name']
    db.session.add(user)
    db.session.commit()
    login_user(user)

    return redirect(url_for('index'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.route('/addbook', methods=['GET', 'POST'])
@login_required
def addbook():
    form = AddBookForm(request.form)
    if request.method == 'POST' and form.validate():
        newbook = BookRecord()
        newbook.name = form.name.data
        newbook.create_user = current_user.id
        newbook.author = form.author.data
        newbook.book_type = form.book_type.data
        newbook.description = form.description.data
        newbook.language = form.language.data
        newbook.target_place = form.target_place.data
        newbook.price = form.price.data
        newbook.service_type = form.service_type.data
        newbook.is_exchanged = False

        db.session.add(newbook)
        db.session.commit()

        if request.files['image'].filename != '':
            imagedata = request.files['image'].read()
            base64code = base64.b64encode(imagedata)
            recordimg = RecordImage()
            recordimg.record = newbook.id
            recordimg.image = base64code
            db.session.add(recordimg)
            db.session.commit()

        return redirect(url_for('index'))

    return render_template('addbook.html',
                           title='Add a book',
                           form=form)


# @app.route('/bookdetail', methods=['GET', 'POST'])
# def
