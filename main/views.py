# -*- coding: utf-8 -*-
import hashlib
import re
from main import main
from flask import render_template, g, request, redirect, url_for, jsonify
from flask_login import current_user, login_required, login_user, LoginManager, logout_user
from main.database import Users, Session, Votes, Research
from sqlalchemy import and_, or_, desc, distinct
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.sql import func
from random import shuffle


login_manager = LoginManager()
login_manager.init_app(main)
login_manager.session_protection = "strong"
csrf = CSRFProtect(main)

global_type_research = ['famous_people', 'plants', 'animals', 'nature_object']


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


@main.route('/admin/', methods=['GET', 'POST'])
def index():
    return render_template('15open.html')


@main.route('/', methods=['GET'])
@main.route('/main', methods=['GET'])
def test():
    users = []
    all_user = g.db.query(Users.id.label('user_id'), Users.FIO, Users.age).all()
    for i in all_user:
        check_research = g.db.query(Research.id, Research.main_photo_path).filter(Research.user_id == i.user_id).first()
        if check_research:
            count_research = g.db.query(Research).filter(Research.user_id == i.user_id).count()
            count_votes = g.db.query(Votes).filter(Votes.user_research == i.user_id).count()
            users.append([i, check_research.id, check_research.main_photo_path, count_research, count_votes])
    users = sorted(users[0:4], key=lambda x: x[4], reverse=True) if users != [] else None

    research_famous_people = g.db.query(
        Research.id,
        Research.name,
        Research.main_photo_path,
        Users.FIO
    ).join(
        Users,
        Users.id == Research.user_id,
        isouter=True
    ).filter(Research.type_research == 'famous_people').all()
    shuffle(research_famous_people)
    research_famous_people = research_famous_people[0:4]

    research_plants = g.db.query(
        Research.id,
        Research.name,
        Research.main_photo_path,
        Users.FIO
    ).join(
        Users,
        Users.id == Research.user_id,
        isouter=True
    ).filter(Research.type_research == 'plants').all()
    shuffle(research_plants)
    research_plants = research_plants[0:4]

    research_animals = g.db.query(
        Research.id,
        Research.name,
        Research.main_photo_path,
        Users.FIO
    ).join(
        Users,
        Users.id == Research.user_id,
        isouter=True
    ).filter(Research.type_research == 'animals').all()
    shuffle(research_animals)
    research_animals = research_animals[0:4]

    research_nature_objects = g.db.query(
        Research.id,
        Research.name,
        Research.main_photo_path,
        Users.FIO
    ).join(
        Users,
        Users.id == Research.user_id,
        isouter=True
    ).filter(Research.type_research == 'nature_object').all()
    shuffle(research_nature_objects)
    research_nature_objects = research_nature_objects[0:4]

    try:
        user_autificate = True if current_user.id else None
    except AttributeError:
        user_autificate = False

    return render_template('index.html',
                           random_users=users,
                           research_famous_people=research_famous_people,
                           research_plants=research_plants,
                           research_animals=research_animals,
                           research_nature_objects=research_nature_objects,
                           user_autificate=user_autificate)


@main.route("/rating", methods=['GET', 'POST'])
def rating():

    users = []

    all_user = g.db.query(Users.id.label('user_id'), Users.FIO, Users.age).all()
    for i in all_user:
        check_research = g.db.query(Research.id, Research.main_photo_path).filter(Research.user_id == i.user_id).first()
        if check_research:
            count_research = g.db.query(Research).filter(Research.user_id == i.user_id).count()
            count_votes = g.db.query(Votes).filter(Votes.user_research == i.user_id).count()
            users.append([i, check_research.id, check_research.main_photo_path, count_research, count_votes])

    users = sorted(users, key=lambda x: x[4], reverse=True) if users != None else users

    return render_template('rating.html', all_user_with_researchs=users)


@main.route('/add_research/<type_research>')
@login_required
def add_research(type_research):
    if type_research not in global_type_research:
        return redirect(url_for('test'))
    return render_template("add_research.html", type_research=type_research)


@main.route('/research/<int:id_research>', methods=['GET', 'POST'])
def research(id_research):
    check_research = g.db.query(
        Research.id,
        Research.name,
        Research.type_research,
        Research.about,
        Research.main_photo_path,
        Research.photos,
        Research.videos,
        Users.FIO,
        Users.city,
        Users.school,
        Users.age
    ).join(
        Users,
        Users.id == Research.user_id
    ).filter(
        Research.id == id_research
    ).first()
    if check_research is None:
        return redirect(url_for('test'))

    try:
        count_votes_user = 3 - int(g.db.query(Votes).filter(Votes.user_vote == current_user.id).count())
        user_autificate = True if current_user.id else None
    except AttributeError:
        user_autificate = False
        count_votes_user = None

    return render_template('research.html', check_research=check_research, user_autificate=user_autificate, count_votes_user=count_votes_user)


@main.route('/category/<type_category>')
def category(type_category):

    if type_category not in global_type_research:
        return redirect(url_for('test'))

    users = []
    get_research_with_categorys = g.db.query(
        Research.id,
        Research.name,
        Research.main_photo_path,
        Users.FIO,
        Users.age,
        Users.id.label('user_id')
    ).join(
        Users,
        Users.id == Research.user_id,
        isouter=True
    ).filter(
        Research.type_research == type_category
    ).all()

    if get_research_with_categorys != [(None, None, None, None, None)]:
        for i in get_research_with_categorys:
            count_research = g.db.query(Research).filter(Research.user_id == i.user_id).count()
            count_votes = g.db.query(Votes).filter(Votes.user_vote_to_research == i.id).count()
            if count_research != 0:
                users.append([i, count_votes])
    else:
        users = None

    try:
        count_votes_user = 3 - int(g.db.query(Votes).filter(Votes.user_vote == current_user.id).count())
        user_autificate = True if current_user.id else None
    except AttributeError:
        user_autificate = False
        count_votes_user = None
    return render_template('category.html',
                           type_category=type_category,
                           get_research_with_categorys=users,
                           count_votes_user=count_votes_user,
                           user_autificate=user_autificate)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))
