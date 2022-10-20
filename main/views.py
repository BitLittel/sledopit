# -*- coding: utf-8 -*-
from main import main
from flask import render_template, g, request, redirect, url_for
from flask_login import current_user, login_required, LoginManager, logout_user
from main.database import Users, Session, Votes, Research
from sqlalchemy import and_, or_, text
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.sql import func


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


@main.route(f'/admin/{main.config["SECRET_KEY"]}', methods=['GET', 'POST'])
def index():
    get_all_researchs = g.db.query(
        Research
    ).filter(
        or_(
            and_(
                Research.checked == 0,
                Research.prichina == None
            ),
            and_(
                Research.checked == 0,
                Research.prichina == ''
            )
        )
    ).all()
    count_users = g.db.query(Users).count()
    count_sledopit = g.db.query(Users).join(Research, Research.user_id == Users.id).group_by(Users.id).count()

    count_sledopit_famous_people = g.db.query(
        Users.id,
        Research.id
    ).join(
        Research,
        Research.user_id == Users.id
    ).filter(
        Research.type_research == 'famous_people'
    ).group_by(Users.id).count()

    count_sledopit_plants = g.db.query(
        Users.id,
        Research.id
    ).join(
        Research,
        Research.user_id == Users.id
    ).filter(
        Research.type_research == 'plants'
    ).group_by(Users.id).count()

    count_sledopit_animals = g.db.query(
        Users.id,
        Research.id
    ).join(
        Research,
        Research.user_id == Users.id
    ).filter(
        Research.type_research == 'animals'
    ).group_by(Users.id).count()

    count_sledopit_nature_object = g.db.query(
        Users.id,
        Research.id
    ).join(
        Research,
        Research.user_id == Users.id
    ).filter(
        Research.type_research == 'nature_object'
    ).group_by(Users.id).count()
    return render_template('admin.html',
                           get_all_researchs=get_all_researchs,
                           count_users=count_users,
                           count_sledopit=count_sledopit,
                           count_sledopit_famous_people=count_sledopit_famous_people,
                           count_sledopit_plants=count_sledopit_plants,
                           count_sledopit_animals=count_sledopit_animals,
                           count_sledopit_nature_object=count_sledopit_nature_object)


@main.route('/', methods=['GET'])
@main.route('/main', methods=['GET'])
def test():
    users = g.db.execute(text("select user.id as user_id, user.FIO, user.age, research.id, research.main_photo_path, (select count(*) from research where research.user_id = user.id and research.checked = 1) as count_research, (select count(*) from votes where votes.user_research = user.id) as count_votes from user join research on user.id = research.user_id where research.checked = 1 group by user.id order by count_votes desc limit 4"))
    users = [x for x in users]

    research_famous_people = g.db.query(
        Research.id,
        Research.name,
        Research.main_photo_path,
        Users.FIO
    ).join(
        Users,
        Users.id == Research.user_id,
        isouter=True
    ).filter(
        and_(Research.type_research == 'famous_people', Research.checked == True)
    ).order_by(func.rand()).limit(4).all()

    research_plants = g.db.query(
        Research.id,
        Research.name,
        Research.main_photo_path,
        Users.FIO
    ).join(
        Users,
        Users.id == Research.user_id,
        isouter=True
    ).filter(
        and_(Research.type_research == 'plants', Research.checked == True)
    ).order_by(func.rand()).limit(4).all()

    research_animals = g.db.query(
        Research.id,
        Research.name,
        Research.main_photo_path,
        Users.FIO
    ).join(
        Users,
        Users.id == Research.user_id,
        isouter=True
    ).filter(
        and_(Research.type_research == 'animals', Research.checked == True)
    ).order_by(func.rand()).limit(4).all()

    research_nature_objects = g.db.query(
        Research.id,
        Research.name,
        Research.main_photo_path,
        Users.FIO
    ).join(
        Users,
        Users.id == Research.user_id,
        isouter=True
    ).filter(
        and_(Research.type_research == 'nature_object', Research.checked == True)
    ).order_by(func.rand()).limit(4).all()

    try:
        user_autificate = True if current_user.id else None
    except AttributeError:
        user_autificate = False

    return render_template('index.html',
                           top_users=users,
                           research_famous_people=research_famous_people,
                           research_plants=research_plants,
                           research_animals=research_animals,
                           research_nature_objects=research_nature_objects,
                           user_autificate=user_autificate)


@main.route("/rating", methods=['GET', 'POST'])
def rating():
    users = g.db.execute(text("select user.id as user_id, user.FIO, user.age, research.id, research.main_photo_path, (select count(*) from research where research.user_id = user.id and research.checked = 1) as count_research, (select count(*) from votes where votes.user_research = user.id) as count_votes from user join research on user.id = research.user_id where research.checked = 1 group by user.id order by count_votes desc"))
    users = [x for x in users]
    return render_template('rating.html', top_users=users)


@main.route('/winners', methods=['POST', 'GET'])
def winners():
    return render_template('winners.html')


# @main.route('/add_research/<type_research>')
# @login_required
# def add_research(type_research):
#     if type_research not in global_type_research:
#         return redirect(url_for('test'))
#     return render_template("add_research.html", type_research=type_research)


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
        Research.checked,
        Research.prichina,
        Research.user_id,
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

    all_research_user = g.db.query(
        Research.id,
        Research.name,
        Research.type_research,
        Research.main_photo_path
    ).filter(and_(Research.id != check_research.id, Research.user_id == check_research.user_id)).all()

    try:
        count_votes_user = 3 - int(g.db.query(Votes).filter(Votes.user_vote == current_user.id).count())
        user_autificate = True if current_user.id else None
    except AttributeError:
        user_autificate = False
        count_votes_user = None

    return render_template('research.html',
                           check_research=check_research,
                           user_autificate=user_autificate,
                           count_votes_user=count_votes_user,
                           all_research_user=all_research_user)


@main.route('/category/<type_category>')
def category(type_category):

    if type_category not in global_type_research:
        return redirect(url_for('test'))

    try:
        count_votes_user = 3 - int(g.db.query(Votes).filter(Votes.user_vote == current_user.id).count())
        user_autificate = True if current_user.id else None
    except AttributeError:
        user_autificate = False
        count_votes_user = None

    users = []
    filter_cat = [and_(Research.type_research == type_category, or_(Research.user_id == current_user.id, Research.checked == True))] if user_autificate else [and_(Research.type_research == type_category, Research.checked == True)]
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
    ).filter(*filter_cat).all()

    if get_research_with_categorys != [(None, None, None, None, None)]:
        for i in get_research_with_categorys:
            count_research = g.db.query(Research).filter(Research.user_id == i.user_id).count()
            count_votes = g.db.query(Votes).filter(Votes.user_vote_to_research == i.id).count()
            if count_research != 0:
                users.append([i, count_votes])
    else:
        users = None

    return render_template('category.html',
                           type_category=type_category,
                           get_research_with_categorys=users,
                           count_votes_user=count_votes_user,
                           user_autificate=user_autificate)


@main.route('/edit_research/<int:id_research>', methods=['GET', 'POST'])
@login_required
def edit_research(id_research):
    check_research = g.db.query(Research).filter(Research.id == id_research).first()
    if check_research == None:
        return redirect(url_for('test'))
    if check_research.user_id != current_user.id:
        return redirect(url_for('test'))
    return render_template("edit_research.html", check_research=check_research)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))
