import hashlib
import re
from main import main
from flask import render_template, g, request, redirect, url_for, jsonify
from flask_login import current_user, login_required, login_user, LoginManager, logout_user
from main.database import Users, Session, Cites
from sqlalchemy import and_, or_, desc
from flask_wtf.csrf import CSRFProtect


@main.route('/api/login', methods=['POST', 'GET'])
def api_login():
    if request.method == 'GET':
        phoneNumber = request.args.get('phoneNumber').strip().replace(' ', '').replace('(', '').replace(')', '')
        if re.search(r'^(([+][0-9]{1,3})[0-9]{10})|(8+[0-9]{10})$', phoneNumber) is None:
            return jsonify(dict(login=False, header='Ошибка', text='Номер телефона введён некорректно'))
        check_user = g.db.query(Users).filter(Users.tel_number == phoneNumber).first()
        if check_user:
            login_user(check_user, remember=True)
            return jsonify(dict(login=True))
        else:
            return jsonify(dict(login='not found user'))


@main.route('/api/reg', methods=['POST', 'GET'])
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
        phoneNumber = request.args.get('phoneNumber')
        # Проверка имени и фамилии
        name = request.args.get('name')
        if re.search(r'^([а-яА-Я]{2,30}) ([а-яА-Я]{2,30})$', name) is None:
            return jsonify(dict(
                reg=False,
                header='Ошибка',
                text='Поле "Фамилия Имя" введено некорректно'))
        # школу пока тоже не буду проверять, т.к не понятно
        school = request.args.get('school')
        # Проверка возраста
        try:
            ageSelection = int(request.args.get('ageSelection'))
        except ValueError:
            return jsonify(dict(
                reg=False,
                header='Ошибка',
                text='Поле "Возраст" введено некорректно'))
        # Проверка города
        cityFrom = request.args.get('cityFrom')
        if g.db.query(Cites).filter(Cites.name_city == cityFrom).first() is None:
            return jsonify(dict(
                reg=False,
                header='Ошибка',
                text='Поле "Откуда ты" введено некорректно'))

        new_user = Users(FIO=name, tel_number=phoneNumber, city=cityFrom, school=school, age=ageSelection)
        g.db.add(new_user)
        g.db.commit()
        login_user(new_user, remember=True)
        return jsonify(dict(reg=True))