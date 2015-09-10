# This package may contain traces of nuts

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from sqlalchemy.exc import SQLAlchemyError

engine = create_engine("postgresql+psycopg2://pom:pom00@localhost:5432/pom", pool_size=20, max_overflow=100)
Session = sessionmaker(bind=engine)

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e: 
        session.rollback()
        
        try:
            raise e             
        except SQLAlchemyError as e:
            raise BstTechnicalError("SQLAlchemyError") from e
        except Exception as e:
            print("**** unhandeled exception")
            raise         
    finally:
        session.close()
        
# TODO move this to somewhere else
        
class BstError(Exception):
    """Generic error class."""
    
class BstTechnicalError(BstError):
    """Base for all technical ie non semantic errors"""