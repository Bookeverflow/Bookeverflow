import base64
import json
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
            'description': record.description if len(record.description) < 100 \
        else record.description[:100] + '...',
            'service_type': record.service_type,
            'language': record.language
        } for record in bookrecords]
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
        newbook.service_type = request.form['service_type']
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


@app.route('/bookdetail/<record_uuid>', methods=['GET', 'POST'])
def bookdetail(record_uuid):
    book = BookRecord.query.filter_by(uuid=record_uuid).first()
    current_owner = User.query.filter_by(id=book.create_user).first()
    existed_request = DealRequest.query\
                                 .filter_by(requester=current_user.id)\
                                 .filter_by(record=book.id)\
                                 .first()
    requested = False if not existed_request else True
    return render_template('bookdetail.html',
                           title=book.name,
                           book=book,
                           current_owner=current_owner,
                           requested=requested)


@app.route('/makedeal/<record_uuid>', methods=['POST'])
def deal_request(record_uuid):
    bookrecord = BookRecord.query.filter_by(uuid=record_uuid).first()
    if not bookrecord:
        return json.dumps({'success': False}), 400, {'ContentType':'application/json'}

    existed_request = DealRequest.query\
                                 .filter_by(requester=current_user.id)\
                                 .filter_by(record=bookrecord.id)\
                                 .first()
    if existed_request:
        return json.dumps({'success': False}), 400, {'ContentType':'application/json'}

    newrequest = DealRequest()
    newrequest.requester = current_user.id
    newrequest.dealer = bookrecord.create_user
    newrequest.record = bookrecord.id
    db.session.add(newrequest)
    db.session.commit()
    return json.dumps({'success': True}), 200, {'ContentType':'application/json'}


@app.route('/check_request')
def check_request():
    allrequest = DealRequest.query.filter_by(requester=current_user.id).all()
    datas = []
    for r in allrequest:
        progress = 'Not Yet'
        if r.processed:
            progress = 'Accepted' if r.accepted else 'Rejected'
        datas.append({
            'progress': progress,
            'b': r.get_book()
        })
    return render_template('check_request.html',
                           title='Request List',
                           datas=datas)


@app.route('/check_deal')
def check_deal():
    allrequest = DealRequest.query.filter_by(dealer=current_user.id).all()
    datas = []
    for r in allrequest:
        result = None
        if r.processed:
            result = 'Accepted' if r.accepted else 'Rejected'
        datas.append({
            'result': result,
            'processed': r.processed,
            'requester': User.query.filter_by(id=r.requester).first(),
            'b': r.get_book()
        })
    return render_template('check_deal.html',
                           title='Deal List',
                           datas=datas)


@app.route('/makefinaldeal/<record_uuid>', methods=['POST'])
def deal_decision(record_uuid):
    bookrecord = BookRecord.query.filter_by(uuid=record_uuid).first()
    if not bookrecord:
        return json.dumps({'success': False}), 400, {'ContentType':'application/json'}

    thisrequest = DealRequest.query\
                             .filter_by(requester=current_user.id)\
                             .filter_by(record=bookrecord.id)\
                             .first()
    if not thisrequest:
        return json.dumps({'success': False}), 400, {'ContentType':'application/json'}

    decision = request.values.get('accept', None)

    if decision is None:
        return json.dumps({'success': False}), 400, {'ContentType':'application/json'}

    thisrequest.processed = True
    thisrequest.accepted = decision == 'true'
    db.session.commit()
    return json.dumps({'success': True}), 200, {'ContentType':'application/json'}
