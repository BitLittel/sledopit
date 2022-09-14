# -*- coding: utf-8 -*-
import hashlib
import re
from main import main
from flask import render_template, g, request, redirect, url_for, jsonify
from flask_login import current_user, login_required, login_user, LoginManager, logout_user
from main.database import Users, Session, Cites, Votes, Research
from sqlalchemy import and_, or_, desc
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


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('15open.html')


# todo: почле открытия поставить как "/" и "/index"
@main.route('/main', methods=['GET', 'POST'])
def test():
    users = []
    all_researchs_with_user = g.db.query(
        Research.id,
        Research.main_photo_path,
        Users.FIO,
        Users.age,
        Users.id.label('user_id')
    ).join(
        Users,
        Users.id == Research.user_id
    ).all()

    for i in all_researchs_with_user:
        count_research = g.db.query(Research).filter(Research.user_id == i.user_id).count()
        count_votes = g.db.query(Votes).filter(Votes.user_vote_to_research == i.id).count()
        if count_research != 0:
            users.append([i, int(count_research), int(count_votes)])

    if users != []:
        shuffle(users)
        users = users[0:4]
    else:
        users = None

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

    return render_template('index.html',
                           random_users=users,
                           research_famous_people=research_famous_people,
                           research_plants=research_plants,
                           research_animals=research_animals,
                           research_nature_objects=research_nature_objects)


@main.route("/rating", methods=['GET', 'POST'])
def rating():
    users = []
    all_researchs_with_user = g.db.query(
        Research.id,
        Research.main_photo_path,
        Users.FIO,
        Users.age,
        Users.id.label('user_id')
    ).join(
        Users,
        Users.id == Research.user_id
    ).all()

    for i in all_researchs_with_user:
        count_research = g.db.query(Research).filter(Research.user_id == i.user_id).count()
        count_votes = g.db.query(Votes).filter(Votes.user_vote_to_research == i.id).count()
        if count_research != 0:
            users.append([i, int(count_research), int(count_votes)])

    users = sorted(users, key=lambda x: x[2], reverse=False) if users != [] else None
    return render_template('rating.html', all_user_with_researchs=users)


@main.route('/add_research/<type_research>')
@login_required
def add_research(type_research):
    if type_research not in global_type_research:
        return redirect(url_for('test'))
    cites = g.db.query(Cites).all()
    return render_template("add_research.html", type_research=type_research, cites=cites)


@main.route('/research/<int:id_research>', methods=['GET', 'POST'])
def research(id_research):
    check_research = g.db.query(
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
    return render_template('research.html', check_research=check_research)


@main.route('/category/<type_category>')
def category(type_category):
    # todo: вывод иследований по категориям
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
    print(get_research_with_categorys)

    if get_research_with_categorys != [(None, None, None, None, None)]:
        for i in get_research_with_categorys:
            count_research = g.db.query(Research).filter(Research.user_id == i.user_id).count()
            count_votes = g.db.query(Votes).filter(Votes.user_vote_to_research == i.id).count()
            print(count_votes)
            if count_research != 0:
                users.append([i, count_votes])
    else:
        users = None

    count_votes_user = 3 - int(g.db.query(Votes).filter(Votes.user_vote == current_user.id).count())
    print(users)
    return render_template('category.html',
                           type_category=type_category,
                           get_research_with_categorys=users if users != None else None,
                           count_votes_user=count_votes_user)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))
