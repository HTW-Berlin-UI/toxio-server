import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

_engine = None

def make_dsn():
    """get db-config from environment"""
    db_user = os.environ.get("DB_USER", "root")
    db_pass = os.environ.get("DB_PASS", "root")
    db_host = os.environ.get("DB_HOST", "localhost")
    db_name = os.environ.get("DB_NAME", "chem_scan")

    db_dsn = "mysql+mysqlconnector://{}:{}@{}/{}".format(db_user, db_pass,
                                                         db_host, db_name)

    return db_dsn

def make_session(engine):
    """establishes a connection to the db"""


    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()

    return session




def get_session():
    global _engine

    if _engine == None:
        db_dsn = make_dsn()
        _engine = create_engine(db_dsn, echo=True)

    return make_session(_engine)









