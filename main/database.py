# -*- coding: utf-8 -*-
from main import main
from sqlalchemy import Column, create_engine, DateTime, Text, Unicode, Boolean, ForeignKey, Date, BigInteger, Integer,\
    PickleType, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm.scoping import scoped_session

Base = declarative_base()


class Users(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    FIO = Column(Unicode(255, collation='utf8_unicode_ci'), nullable=False)
    tel_number = Column(Unicode(128, collation='utf8_unicode_ci'), nullable=False)
    city = Column(Unicode(128, collation='utf8_unicode_ci'))
    school = Column(Unicode(255, collation='utf8_unicode_ci'))
    age = Column(Integer)
    password = Column(Unicode(255, collation='utf8_unicode_ci'))

    users_votes = relationship('Votes', backref='users_votes', lazy='dynamic')
    researches_users = relationship('Research', backref='researches_users', lazy='dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def __repr__(self):
        return "<User(%r, %r, %r)>" % (self.id, self.FIO, self.tel_number)


class Research(Base):
    __tablename__ = 'research'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(Users.id))
    name = Column(Unicode(255, collation='utf8_unicode_ci'))
    type_research = Column(Enum('famous_people', 'plants', 'animals', 'nature_object'), default='famous_people')
    about = Column(Text(collation='utf8_unicode_ci'))
    main_photo_path = Column(Unicode(255, collation='utf8_unicode_ci'))
    photos = Column(PickleType, default=list())
    videos = Column(PickleType, default=list())
    checked = Column(Boolean, default=False)
    prichina = Column(Unicode(255, collation='utf8_unicode_ci'), default=None)

    research_votes = relationship('Votes', backref='research_votes', lazy='dynamic')


class Votes(Base):
    __tablename__ = 'votes'
    id = Column(Integer, primary_key=True)
    user_vote = Column(Integer, ForeignKey(Users.id))
    user_vote_to_research = Column(Integer, ForeignKey(Research.id))
    user_research = Column(Integer)


engine = create_engine('mysql+pymysql://%s:%s@%s/%s?charset=utf8' % (main.config['DATABASE_USER'],
                                                                     main.config['DATABASE_PASSWORD'],
                                                                     main.config['DATABASE_IP'],
                                                                     main.config['DATABASE_NAME']),
                       encoding='utf8', echo=False, pool_recycle=300, query_cache_size=0, pool_pre_ping=True)
Base.metadata.create_all(engine)

Session = scoped_session(sessionmaker())
Session.configure(bind=engine)  # конфигурируем сессию с БД
