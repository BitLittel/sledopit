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
        ).order_by(func.rand()).limit(4).all()
        users = []
        for i in rand_user:
            count_research = db.query(Research).filter(and_(Research.user_id == i.user_id, Research.checked == True)).count()
            count_votes = db.query(Votes).join(Research, Research.id == Votes.user_vote_to_research).filter(and_(Votes.user_research == i.user_id, Research.checked == True)).count()
            users.append([i, count_research, count_votes])
        end = time.time()
        print(f'delta: {end-start}')
        print(users)

        print('kek2')
        start = time.time()
        users = []
        all_user = db.query(Users.id.label('user_id'), Users.FIO, Users.age).all()
        for i in all_user:

            check_research = db.query(
                Research.id,
                Research.main_photo_path
            ).filter(
                and_(Research.user_id == i.user_id, Research.checked == True)
            ).first()

            if check_research:
                count_research = db.query(
                    Research
                ).filter(
                    and_(Research.user_id == i.user_id, Research.checked == True)
                ).count()

                count_votes = db.query(
                    Votes
                ).join(
                    Research,
                    Research.id == Votes.user_vote_to_research
                ).filter(
                    and_(Votes.user_research == i.user_id, Research.checked == True)
                ).count()

                users.append([i, check_research.id, check_research.main_photo_path, count_research, count_votes])
        users = sorted(users, key=lambda x: x[4], reverse=True) if users != [] else None
        end = time.time()
        print(f'delta: {end - start}')
        print(users)

        # print('kek2')
        # start = time.time()
        # get_id_min_max = db.query(func.max(Users.id).label('max'), func.min(Users.id).label('min')).first()
        # print(f'min: {get_id_min_max.min} max: {get_id_min_max.max}')
        # rand_arr_int = []
        # for i in range(4):
        #     r = randint(get_id_min_max.min, get_id_min_max.max)
        #     if r not in rand_arr_int:
        #         rand_arr_int.append(r)
        # print(rand_arr_int)
        # test_test = db.query(Users).filter(Users.id in rand_arr_int).all()
        # print(f'test: {test_test}')
        # users = []
        # for i in rand_arr_int:
        #     rand_user = db.query(
        #         Users.id.label('user_id'),
        #         Users.FIO,
        #         Users.age,
        #         Research.id,
        #         Research.main_photo_path
        #     ).join(
        #         Research,
        #         Research.user_id == Users.id
        #     ).filter(
        #         and_(Research.checked == True, Users.id == i)
        #     ).first()
        #
        #     print('User_rand:', rand_user)
        #
        #     count_research = db.query(Research).filter(and_(Research.user_id == rand_user.user_id, Research.checked == True)).count()
        #
        #     count_votes = db.query(Votes).join(Research, Research.id == Votes.user_vote_to_research).filter(
        #         and_(Votes.user_research == rand_user.user_id, Research.checked == True)).count()
        #
        #     users.append([rand_user, count_research, count_votes])
        #
        # print(users)
        # end = time.time()
        # print(f'delta: {end - start}')
        # print('finish')


if __name__ == '__main__':
    test()
