# This package may contain traces of nuts

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.dialects import postgresql
import logging
logger = logging.getLogger(__name__)

engine = create_engine("postgresql+psycopg2://pom:pom00@localhost:5432/pom", pool_size=20, max_overflow=100)
Session = sessionmaker(bind=engine)

def dumpStatement(query):
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug('Dump SQL Statement:\n%s', str(query.statement.compile(dialect=postgresql.dialect())))

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
            raise BstSystemError() from e        
    finally:
        session.close()
        
# TODO move this to somewhere else
        
class BstError(Exception):
    """Generic error class."""
    
class BstSystemError(BstError):
    """AttributeError ..."""    
    
class BstTechnicalError(BstError):
    """Base for all technical ie non business errors"""
    
class BstValidationError(BstTechnicalError):
    """Whenever user input is not valid""" 
    
class BstAuthorizationError(BstTechnicalError):
    """Whenever a user is not allowed""" 
      
    
    