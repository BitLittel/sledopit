# -*- coding: utf-8 -*-

import hashlib
import re
from main import main
from flask import render_template, g, request, redirect, url_for, jsonify
from flask_login import current_user, login_required, login_user, LoginManager, logout_user
from main.database import Users, Session, Cites
from sqlalchemy import and_, or_, desc
from flask_wtf.csrf import CSRFProtect


login_manager = LoginManager()
login_manager.init_app(main)
login_manager.session_protection = "strong"

csrf = CSRFProtect(main)


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


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('15open.html')


# todo: почле открытия поставить как "/" и "/index"
@main.route('/main')
def test():
    get_city = g.db.query(Cites).all()
    return render_template('index.html', cites=get_city)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))
