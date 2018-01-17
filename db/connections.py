import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

_session = None

def make_dsn():
    """get db-config from environment"""
    db_user = os.environ.get("DB_USER", "root")
    db_pass = os.environ.get("DB_PASS", "root")
    db_host = os.environ.get("DB_HOST", "localhost")
    db_name = os.environ.get("DB_NAME", "chem_scan")

    db_dsn = "mysql+mysqlconnector://{}:{}@{}/{}".format(db_user, db_pass,
                                                         db_host, db_name)

    return db_dsn

def make_session():
    """establishes a connection to the db"""

    db_dsn = make_dsn()
    engine = create_engine(db_dsn, echo=True)

    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()

    return session




def get_session():
    global _session

    if _session == None:
        _session = make_session()

    return _session









