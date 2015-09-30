# This package may contain traces of nuts

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from sqlalchemy.exc import SQLAlchemyError

import logging
logger = logging.getLogger(__name__)

__connectstring__ = None
__dialect__ = None
Session = None
dialect_module = None

def getSession():
    '''
    getSession expects the module variable __connectstring__ being set outside of bst.pygasus.rdb to
    a connect string in following format:
                     postgresql+psycopg2://pom:pom00@localhost:5432/pom
                     
    Put the following lines to your startup class:
    
    from bst.pygasus import rdb
        rdb.__connectstring__ = 'postgresql+psycopg2://pom:pom00@localhost:5432/pom'
        rdb.__dialect__ = 'postgresql'
    '''
    global Session
    if Session is None:
        if __connectstring__ is None:
           raise BstSystemError('Mandatory module variable __connectstring__ not set!') 
        
        logger.info('Creating Session and bind engine with connect string: %s', __connectstring__)
        try:
            engine = create_engine(__connectstring__, pool_size=20, max_overflow=100)
            Session = sessionmaker(bind=engine)
        except Exception as e:
            raise BstSystemError() from e
    return Session()

def getDialect():
    '''getDialect expects the module variable __dialect__ being set outside of bst.pygasus.rdb to
       a valid sqlalchemy dialect contained in package sqlalchemy.dialects.
       
        Put the following lines to your startup class:
    
        from bst.pygasus import rdb
            rdb.__connectstring__ = 'postgresql+psycopg2://pom:pom00@localhost:5432/pom'
            rdb.__dialect__ = 'postgresql'
    '''  
    
    global dialect_module
    if dialect_module is None:
        if __dialect__ is None:
           raise BstSystemError('Mandatory module variable __dialect__ not set!') 
               
        logger.debug('Loading dialect module %s', __dialect__)
        try:
            dialect_module = __import__('sqlalchemy.dialects.%s' % __dialect__, fromlist=[__dialect__])
        except ImportError as e:
            raise BstSystemError('Database dialect %s not found in sqlalchemy.dialects' % __dialect__) from e
        logger.info('Dialect module %s successfully loaded', dialect_module.__name__)                    
    return dialect_module.dialect()

def dumpStatement(query):
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug('Dump SQL Statement:\n%s', str(query.statement.compile(dialect=getDialect())))

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = getSession()
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
      
    
    