# -*- coding: utf-8 -*-

import hashlib
import re
from main import main
from flask import render_template, g, request, redirect, url_for, jsonify
from flask_login import current_user, login_required, login_user, LoginManager, logout_user
from main.database import Users, Session
from sqlalchemy import and_, or_, desc


login_manager = LoginManager()
login_manager.init_app(main)


@main.before_request
def before_request():
    g.db = Session()


@login_manager.user_loader
def load_user(uid):
    return g.db.query(Users).filter_by(id=uid).first()


@login_manager.unauthorized_handler
def unauth():
    return redirect(url_for("login", next=request.path))


@main.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404


@main.errorhandler(500)
def internal_error(error):
    g.db.rollback()
    return render_template('500.html'), 500


@main.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@main.route('/login', methods=['GET', 'POST'])
def login():
    tel = None
    fio = None
    if request.method == 'GET':
        fio = request.args.get('FIO')
        tel = request.args.get('tel')
        if fio is not None and tel is not None:
            if re.search(r'^([а-яА-Я]{2,}) ([а-яА-Я]{2,})(()|( [а-яА-Я]{2,}))$', fio) is None:
                return jsonify(dict(reg_ok=False, input='fio', error="ФИО введено не корректно"))
            if re.search(r'^(([+][0-9]{1,3})[0-9]{10})|(8+[0-9]{10})$', tel) is None:
                return jsonify(dict(reg_ok=False, input='tel', error="Номер телефона введён не корректно"))
            return jsonify(dict(reg_ok=True))

    if request.method == 'POST':
        fio = request.form.get('FIO')
        tel = request.form.get('tel')

        if re.search(r'^([а-яА-Я]{2,}) ([а-яА-Я]{2,})(()|( [а-яА-Я]{2,}))$', fio) is None:
            return render_template('login.html', fio=fio, tel=tel, input='fio')
        if re.search(r'^(([+][0-9]{1,3})[0-9]{10})|(8+[0-9]{10})$', tel) is None:
            return render_template('login.html', fio=fio, tel=tel, input='tel')

        get_user = g.db.query(Users).filter(and_(Users.FIO == fio, Users.tel_number == tel)).first()
        if get_user is None:
            get_user = Users(FIO=fio, tel_number=tel)
            g.db.add(get_user)
            g.db.commit()
        login_user(get_user, remember=True)
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        else:
            return redirect(url_for('index'))
    return render_template('login.html', fio=fio, tel=tel)


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')


@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))
