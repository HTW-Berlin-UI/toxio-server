from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

_session = None

def make_session():
    """establishes a connection to the db"""

    engine = create_engine(
        'mysql+mysqlconnector://root:123@localhost/chemscan', echo=True)

    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()

    return session


def get_session():
    global _session

    if _session == None:
        _session = make_session()

    return _session









