from flask import Flask
# from contextlib import contextmanager
# from main.database import Session

main = Flask(__name__)
main.config.from_object('config')


# @contextmanager
# def session_scope():
#     session = Session()
#     try:
#         yield session
#         session.commit()
#     except:
#         session.rollback()
#         raise
#     finally:
#         session.close()


# with session_scope() as db:
from main import views
