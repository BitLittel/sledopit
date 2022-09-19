# -*- coding: utf-8 -*-
from main.database import Users, Session, Votes, Research
from sqlalchemy import and_, or_, desc, distinct
from sqlalchemy.sql import func
from random import randint
import time


def test():
    with Session() as db:
        print('kek1')
        start = time.time()
        rand_user = db.query(
            Users.id.label('user_id'),
            Users.FIO,
            Users.age,
            Research.id,
            Research.main_photo_path
        ).join(
            Research,
            Research.user_id == Users.id
        ).filter(
            and_(Research.checked == True)
        ).order_by(func.rand()).all()
        print(rand_user)
        end = time.time()
        print(f'delta: {end-start}')

        print('kek1')
        start = time.time()
        get_id_min_max = db.query(func.max(Users.id).label('max'), func.min(Users.id).label('min')).first()
        rand_arr_int = []
        for i in range(4):
            r = randint(get_id_min_max.min, get_id_min_max.max)
            if r not in rand_arr_int:
                rand_arr_int.append(r)
        print(rand_arr_int)

        users = []
        for i in rand_arr_int:
            rand_user = db.query(
                Users.id.label('user_id'),
                Users.FIO,
                Users.age,
                Research.id,
                Research.main_photo_path
            ).join(
                Research,
                Research.user_id == Users.id
            ).filter(
                and_(Research.checked == True, Users.id == i)
            ).first()
            print(rand_user)
            count_research = db.query(Research).filter(
                and_(Research.user_id == rand_user.user_id, Research.checked == True)).count()

            count_votes = db.query(Votes).join(Research, Research.id == Votes.user_vote_to_research).filter(
                and_(Votes.user_research == rand_user.user_id, Research.checked == True)).count()

            users.append([rand_user, count_research, count_votes])

        print(users)
        end = time.time()
        print(f'delta: {end - start}')
        print('finish')


if __name__ == '__main__':
    test()