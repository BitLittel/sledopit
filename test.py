# -*- coding: utf-8 -*-
from main.database import Users, Session, Votes, Research
from sqlalchemy import and_, text
from sqlalchemy.sql import func
import time


def test():
    with Session() as db:

        print('lol')
        start = time.time()
        user = db.execute(text("select user.id as user_id, user.FIO, user.age, research.id, research.main_photo_path, (select count(*) from research where research.user_id = user.id and research.checked = 1) as count_research, (select count(*) from votes where votes.user_research = user.id) as count_votes from user join research on user.id = research.user_id where research.checked = 1 group by user.id order by count_votes desc limit 4"))
        end = time.time()
        print(f'delta: {end - start}')

        user = [x for x in user]
        for i in user:
            print(f'{i.user_id} {i.FIO} {i.age} {i.id} {i.main_photo_path} {i.count_research} {i.count_votes}')

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
        ).filter(Research.checked == True).group_by(Users.id).all()

        users = []
        for i in rand_user:
            count_votes = db.query(Votes).join(Research, Research.id == Votes.user_vote_to_research).filter(
                and_(Votes.user_research == i.user_id, Research.checked == True)
            ).count()
            users.append([i, count_votes])
        users = sorted(users, key=lambda x: x[1], reverse=True)[0:4] if users != [] else None

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

        print('test010')
        start = time.time()

        research_famous_people = db.query(
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

        research_plants = db.query(
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

        research_animals = db.query(
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

        research_nature_objects = db.query(
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

        print(research_famous_people)
        print(research_plants)
        print(research_animals)
        print(research_nature_objects)
        end = time.time()
        print(f'delta: {end - start}')


def test1():
    with Session() as db:

        all = db.query(Users.id, Users.FIO, Users.tel_number).join(Research, Research.user_id == Users.id).all()
        for i in all:
            count_research = db.query(Research).filter(Research.user_id == i.id).count()
            if count_research == 1:
                status = 'Юный исследователь'
            elif count_research == 2:
                status = 'Следопыт'
            elif count_research == 3 or count_research > 3:
                status = 'Следопыт-супергерой'
            print(f"ФИО: {i.FIO}; Телефон: {i.tel_number}; Статус: {status}; Кол-во ислед.: {count_research};")
        # alleay = db.query(Research).filter(Research.id == 270).first()
        # alleay.videos = ["alleay_svezd.mp4"]
        # db.commit()
        #
        # suslin = db.query(Research).filter(Research.id == 269).first()
        # suslin.videos = ["suslin_aleksey_boecz.mp4"]
        # db.commit()
        #
        # ludmila = db.query(Research).filter(Research.id == 268).first()
        # ludmila.videos = ["buzunova_ludmila.mp4"]
        # db.commit()
        #
        # svincov = db.query(Research).filter(Research.id == 252).first()
        # svincov.videos = ["lev_shalupin_svencov.mp4"]
        # db.commit()
        #
        # kedr = db.query(Research).filter(Research.id == 255).first()
        # kedr.videos = ["siborskiy_kedr_lev_sh.mp4"]
        # db.commit()
        #
        # aya = db.query(Research).filter(Research.id == 258).first()
        # aya.videos = ["lev_shalupin_aya.mp4"]
        # db.commit()
    print('заебись, чётко')


if __name__ == '__main__':
    test1()
