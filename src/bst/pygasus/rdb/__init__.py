# This package may contain traces of nuts

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from zope.sqlalchemy import register
from contextlib import contextmanager
from sqlalchemy.exc import SQLAlchemyError, DatabaseError
from bst.pygasus.core.exc import BstSystemError, BstTechnicalError
import transaction
from transaction._compat import get_thread_ident


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
            engine = create_engine(__connectstring__, pool_size=20, max_overflow=100, echo=logger.isEnabledFor(logging.DEBUG))
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


def registerSessionEvents(session):
    current = transaction.get();
    if current.description is None:
       raise BstSystemError('Mandatory module variable __dialect__ not set!')
   
    
    logger.debug('Joining transaction with note %s', current.description)
    register(session)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    logger.debug('Context manager session_scope called.')

    
    try:
        session = getSession()
        session.begin(subtransactions=True)
        registerSessionEvents(session)
        yield session
        logger.debug('End of session_scope reached. Committing session now.')
        session.commit()
    except Exception as e: 
        logger.error('Exception occurred in SQLAlchemy session! Rollback session!')
        session.rollback()
        
        try:
            raise e
        except DatabaseError as e:
            raise BstTechnicalError("DatabaseError: " + e.__str__()) from e           
        except SQLAlchemyError as e:
            raise BstTechnicalError("SQLAlchemyError") from e
        except Exception as e:
            raise BstSystemError() from e
