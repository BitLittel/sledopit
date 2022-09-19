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
            Research.main_photo_path,
            func.count(Research.id).label('count_research')
        ).join(
            Research,
            Research.user_id == Users.id
        ).filter(Research.checked == True).group_by(Users.id).limit(4).all()

        users = []
        for i in rand_user:
            count_votes = db.query(Votes).join(Research, Research.id == Votes.user_vote_to_research).filter(and_(Votes.user_research == i.user_id, Research.checked == True)).count()
            users.append([i, count_votes])
        users = sorted(users, key=lambda x: x[1], reverse=True) if users != [] else None
        # users = []
        # for i in rand_user:
        #     count_research = db.query(Research).filter(and_(Research.user_id == i.user_id, Research.checked == True)).count()
        #     count_votes = db.query(Votes).join(Research, Research.id == Votes.user_vote_to_research).filter(and_(Votes.user_research == i.user_id, Research.checked == True)).count()
        #     users.append([i, count_research, count_votes])
        # users = sorted(users, key=lambda x: x[2], reverse=True)[0:4] if users != [] else None
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
        print(users[0:4])

if __name__ == '__main__':
    test()
