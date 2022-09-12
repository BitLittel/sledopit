# -*- coding: utf-8 -*-
import hashlib
import re
from main import main
from flask import render_template, g, request, redirect, url_for, jsonify
from flask_login import current_user, login_required, login_user, LoginManager, logout_user
from main.database import Users, Session, Cites, Votes, PhotoAndVideo, Research
from sqlalchemy import and_, or_, desc
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.sql import func
from random import shuffle


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
    # todo: где test изменить на index
    return redirect(url_for("test", next=request.path))


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

    get_users = g.db.query(Users).all()
    shuffle(get_users)
    random_users = []
    for i in get_users[0:4]:
        count_research = g.db.query(Research).filter(Research.user_id == i.id).count()
        count_votes = g.db.query(Votes).filter(Votes.user_vote_to == i.id).count()
        random_users.append([i, count_research, count_votes])

    research_famous_people = g.db.query(
        Research,
        Users.FIO
    ).join(
        Users,
        Users.id == Research.user_id,
        isouter=True
    ).filter(Research.type_research == 'famous_people').all()

    research_plants = g.db.query(
        Research,
        Users.FIO
    ).join(
        Users,
        Users.id == Research.user_id,
        isouter=True
    ).filter(Research.type_research == 'plants').all()

    research_animals = g.db.query(
        Research,
        Users.FIO
    ).join(
        Users,
        Users.id == Research.user_id,
        isouter=True
    ).filter(Research.type_research == 'animals').all()

    research_nature_objects = g.db.query(
        Research,
        Users.FIO
    ).join(
        Users,
        Users.id == Research.user_id,
        isouter=True
    ).filter(Research.type_research == 'nature_object').all()

    return render_template('index.html',
                           cites=get_city,
                           random_users=random_users,
                           research_famous_people=research_famous_people,
                           research_plants=research_plants,
                           research_animals=research_animals,
                           research_nature_objects=research_nature_objects)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))
