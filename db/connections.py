from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



def make_session():
    """establishes a connection to the db"""

    engine = create_engine(
        'mysql+mysqlconnector://root:root@localhost/chem_scan', echo=True)

    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
    return session











