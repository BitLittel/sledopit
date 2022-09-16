import hashlib
import re
import os
from main import main
from flask import g, request, jsonify
from flask_login import current_user, login_required, login_user
from main.database import Users, Research, Votes
from sqlalchemy import and_
from main.views import global_type_research
from datetime import datetime
from PIL import Image


def hash_password(password: str) -> str:
    h = hashlib.new('sha1')
    h.update(password.encode('utf-8'))
    return h.hexdigest()


def get_path_file_and_save_this(photoAndVideo, id_user):
    if len(photoAndVideo) > 30:
        return 'Максимальное количество файлов не должно превышать 30'
    all_path_photo_and_video = []
    photo_format = ['jpeg', 'png', 'webp']
    video_format = ['mov', 'mp4']

    for i in photoAndVideo:
        type_file = 'mov' if i.content_type == 'video/quicktime' else i.content_type.split('/')[1]
        if (type_file not in photo_format) and (type_file not in video_format):
            return 'Поддерживаемые форматы для фото "jpeg", "png", "webp", для видео "mov", "mp4"'

    for pv in photoAndVideo:
        type_file = 'mov' if pv.content_type == 'video/quicktime' else pv.content_type.split('/')[1]

        random_name = hash_password(f'{pv.filename.split(".")[0]}{id_user}{datetime.now()}')[0:20]

        path_to_download = os.path.join(
            main.config['WORKDIR'],
            "main/static/img/reseach_img",
            f'{random_name}.{type_file}'
        )

        all_path_photo_and_video.append(f'{random_name}.{type_file}')
        pv.save(path_to_download)

    main_photo = ''
    for i in all_path_photo_and_video:
        if i.split('.')[1] in photo_format:
            main_photo = i
            all_path_photo_and_video.remove(i)
            break

    all_photo = []
    for i in all_path_photo_and_video:
        if i.split('.')[1] in photo_format:
            all_photo.append(i)

    all_video = []
    for i in all_path_photo_and_video:
        if i.split('.')[1] in video_format:
            all_video.append(i)

    path_main_photo = os.path.join(main.config['WORKDIR'], "main/static/img/reseach_img", main_photo)
    img_main = Image.open(path_main_photo)
    img_main.save(path_main_photo, quality=70)

    for i in all_photo:
        path_photo = os.path.join(main.config['WORKDIR'], "main/static/img/reseach_img", i)
        img = Image.open(path_photo)
        img.save(path_photo, quality=60)

    return [all_photo, all_video, main_photo]


@main.route('/api/login', methods=['GET'])
def api_login():
    if request.method == 'GET':
        try:
            phoneNumber = request.args.get('phoneNumber').strip().replace(' ', '').replace('(', '').replace(')', '')
            password = request.args.get('loginPassword')
        except:
            return jsonify(dict(login=False, header='Ошибка', text='Номер телефона введён некорректно'))

        if password is None or password == '':
            if re.search(r'^(([+][0-9]{1,3})[0-9]{10})|(8+[0-9]{10})$', phoneNumber) is None:
                return jsonify(dict(login=False, header='Ошибка', text='Номер телефона введён некорректно'))

            check_user = g.db.query(Users).filter(Users.tel_number == phoneNumber).first()
            if check_user is None:
                return jsonify(dict(login='not found user'))
            else:
                return jsonify(dict(login=True))
        else:
            check_user = g.db.query(Users).filter(Users.tel_number == phoneNumber).first()
            if check_user.password == hash_password(password):
                login_user(check_user, remember=True)
                return jsonify(dict(login=True))
            else:
                return jsonify(dict(login=False, header='Ошибка', text='Пароль введен не верно'))


@main.route('/api/reg', methods=['GET'])
def api_reg():
    if request.method == 'GET':
        # проверка галочки согласия на обработку данных
        personalDataAgreement = (request.args.get('personalDataAgreement') == 'true')
        if personalDataAgreement != True:
            return jsonify(dict(
                reg=False,
                header='Ошибка',
                text='Извините, без вашего согласия на обработку, мы не можем вас зарегистрировать'))
        # номер телефона не нужно проверять т.к он уже проверен другим методом
        phoneNumber = request.args.get('phoneNumber').strip().replace(' ', '').replace('(', '').replace(')', '')
        # Проверка имени и фамилии
        name = request.args.get('name').strip()
        if re.search(r'^([а-яА-Я]{2,30}) ([а-яА-Я]{2,30})$', name) is None:
            return jsonify(dict(
                reg=False,
                header='Ошибка',
                text='Поле "Фамилия Имя" введено некорректно'))

        signinPassword = request.args.get('signinPassword')
        if re.search(r'^[a-zA-Z0-9@#$%^&+=_/-]{8,}$', signinPassword) is None:
            return jsonify(dict(
                reg=False,
                header='Ошибка',
                text='Пароль введен не корректно. Могут быть только латинские символы и спец.символы, а так же длинна от 8 символов'))

        new_user = Users(FIO=name, tel_number=phoneNumber, password=hash_password(signinPassword))
        g.db.add(new_user)
        g.db.commit()
        login_user(new_user, remember=True)
        return jsonify(dict(reg=True))


@main.route('/api/load_research', methods=['POST'])
@login_required
def api_load_research():
    if request.method == 'POST' and request.form.get('have_data') and (request.form.get('type_research') in global_type_research):
        if g.db.query(Research).filter(Research.user_id == current_user.id).count() >= 20:
            return jsonify(dict(reseach=False, header='Ошибка', text='Харош дудосить'))
        have_data = request.form.get('have_data') == 'true'
        type_research = request.form.get('type_research')
        photo_and_video = request.files.getlist('photo_and_video')
        newResearchText = request.form.get('newResearchText')
        newResearchName = request.form.get('newResearchName')

        if have_data and current_user.school is not None:

            if newResearchText is None or newResearchText == '':
                return jsonify(dict(reseach=False, header='Ошибка', text='Поле "Текст работы" не заполнено'))
            if len(newResearchText) < 2000:
                return jsonify(dict(reseach=False,  header='Ошибка', text='Дорогой друг, текст слишком короткий. Минимальная длина текста - 2000 символов.'))
            if newResearchName is None or newResearchName == '':
                return jsonify(dict(reseach=False, header='Ошибка', text='Поле "Название работы не заполнено"'))
            if photo_and_video == []:
                return jsonify(dict(reseach=False, header='Ошибка', text='Поле "Фото, видео" не заполнено'))

            files = get_path_file_and_save_this(photoAndVideo=photo_and_video, id_user=current_user.id)
            if type(files) == str:
                return jsonify(dict(reseach=False, header='Ошибка', text=files))
        else:
            cityFrom = request.form.get('cityFrom')
            ageSelection = request.form.get('ageSelection')
            school = request.form.get('school')

            if newResearchText is None or newResearchText == '':
                return jsonify(dict(reseach=False, header='Ошибка', text='Поле "Текст работы" не заполнено'))
            if newResearchName is None or newResearchName == '':
                return jsonify(dict(reseach=False, header='Ошибка', text='Поле "Название работы" не заполнено'))
            if cityFrom is None or cityFrom == '':
                return jsonify(dict(reseach=False, header='Ошибка', text='Поле "Откуда ты" не заполнено'))
            if ageSelection is None or ageSelection == '':
                return jsonify(dict(reseach=False, header='Ошибка', text='Поле "Возраст" не заполнено'))
            if school is None or school == '':
                return jsonify(dict(reseach=False, header='Ошибка', text='Поле "Учебное заведение" не заполнено'))
            if photo_and_video == []:
                return jsonify(dict(reseach=False, header='Ошибка', text='Поле "Фото, видео" не заполнено'))
            files = get_path_file_and_save_this(photoAndVideo=photo_and_video, id_user=current_user.id)
            if type(files) == str:
                return jsonify(dict(reseach=False, header='Ошибка', text=files))
            get_user = g.db.query(Users).filter(Users.id == current_user.id).first()
            get_user.city = cityFrom
            get_user.school = school
            get_user.age = ageSelection
            g.db.commit()

        add_new_research = Research(researches_users=current_user,
                                    name=newResearchName,
                                    type_research=type_research,
                                    about=newResearchText,
                                    main_photo_path=files[2],
                                    photos=files[0],
                                    videos=files[1])
        g.db.add(add_new_research)
        g.db.commit()
        return jsonify(dict(reseach=True, id_research=add_new_research.id))
    else:
        return jsonify(dict(reseach=False, header='Ошибка', text='Отправлены некорректные данные'))


@main.route('/api/vote', methods=['POST', 'GET'])
@login_required
def vote():
    if request.method == 'GET':
        try:
            user_id = int(request.args.get('user_id'))
            id_research = int(request.args.get('id_research'))
        except ValueError:
            return jsonify(dict(vote=False, header='Ошибка', text='Отправлены некорректные данные'))
        if current_user.id != user_id:
            return jsonify(dict(vote=False, header='Ошибка', text='Отправлены некорректные данные'))
        get_research = g.db.query(Research).filter(Research.id == id_research).first()
        if get_research is None:
            return jsonify(dict(vote=False, header='Ошибка', text='Отправлены некорректные данные'))
        if get_research.user_id == user_id:
            return jsonify(dict(vote=False, header='Ошибка', text='За самого себя проголосовать нельзя'))
        if g.db.query(Votes).filter(and_(Votes.user_vote == user_id, Votes.user_vote_to_research == get_research.id)).first():
            return jsonify(dict(vote=False, header='Ошибка', text='За одну и туже работу нельзя проголосовать'))
        if g.db.query(Votes).filter(Votes.user_vote == user_id).count() == 3:
            return jsonify(dict(vote=False, header='Ошибка', text='Вы уже проголосовали максимальное количество раз'))

        new_votes = Votes(users_votes=current_user, research_votes=get_research, user_research=get_research.user_id)
        g.db.add(new_votes)
        g.db.commit()

    return jsonify(dict(vote=True))


@main.route('/api/edit_research', methods=['GET'])
@login_required
def api_edit_research():
    if request.method == 'GET':
        try:
            user_id = int(request.args.get('user_id'))
            id_research = int(request.args.get('id_research'))
        except ValueError:
            return jsonify(dict(edit=False, header='Ошибка', text='Отправлены некорректные данные'))
        if current_user.id != user_id:
            return jsonify(dict(edit=False, header='Ошибка', text='Отправлены некорректные данные'))
        research = g.db.query(Research).filter(and_(Research.id == id_research, Research.user_id == user_id)).first()
        if research is None:
            return jsonify(dict(edit=False, header='Ошибка', text='Отправлены некорректные данные'))
        newResearchName = request.args.get('newResearchName')
        if newResearchName is None or newResearchName == '':
            return jsonify(dict(edit=False, header='Ошибка', text='Поле "Название работы" не заполнено'))
        newResearchText = request.args.get('newResearchText')
        if newResearchText is None or newResearchText == '':
            return jsonify(dict(edit=False, header='Ошибка', text='Поле "Текст работы" не заполнено'))
        if len(newResearchText) < 2000:
            return jsonify(dict(edit=False, header='Ошибка',
                                text='Дорогой друг, текст слишком короткий. Минимальная длина текста - 2000 символов.'))
        research.name = newResearchName
        research.about = newResearchText
        research.checked = False
        research.prichina = None
        g.db.commit()
    return jsonify(dict(edit=True))


@main.route(f'/api/admin/{main.config["SECRET_KEY"]}', methods=['GET'])
def api_admin():
    if request.method == 'GET':
        id_research = int(request.args.get('id_research'))
        accept = (request.args.get('accept') == 'true')
        print(accept, type(accept))
        prichina = request.args.get('prichina') if accept is False else None
        research = g.db.query(Research).filter(Research.id == id_research).first()
        research.checked = accept
        research.prichina = prichina
        g.db.commit()
    return jsonify(dict(admin=True))
