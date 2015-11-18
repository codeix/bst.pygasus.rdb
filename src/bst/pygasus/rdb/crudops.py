'''
Created on 27.08.2015

@author: oexlt
'''

import logging
from bst.pygasus.rdb import session_scope
from bst.pygasus.rdb import getSession
from bst.pygasus.rdb import dumpStatement
from sqlalchemy import func
from sqlalchemy import inspect
from bst.pygasus.core.exc import BstTechnicalError, BstNoSuchEntityError

logger = logging.getLogger(__name__)

class QueryHelper(object):   
    def getOrderStmt(self, column , direction):
        def asc():
            return column.asc()
        def desc():
            return column.desc()
        switch = {"asc":asc, "desc": desc}
        return switch[direction.lower()]()
   
    def getOrderBy(self, table, sorters, default=None):       
        orderByList = list()
        for sort_param in sorters:
            direction = sort_param['direction']
            property = sort_param['property']           
            orderByList.append(self.getOrderStmt(getattr(table, property.lower()), direction))                    
        
        if str(default) not in [str(i) for i in orderByList]:
            orderByList.append(default)  
                                
        return orderByList
    

def getAllPaged(entityClass, start, limit, sorters, filters, parser):
    logger.debug('getAllPaged called')
    
    helper = QueryHelper()
       
    with session_scope() as session:
        result = (session.query(entityClass)
                  .filter(parser.parseFilter(entityClass, filters))
                  .order_by(*helper.getOrderBy(entityClass, sorters, entityClass.id.asc()))
                  .limit(limit)
                  .offset(start))
                      
        totalCount = session.query(func.count(entityClass.id)).scalar()
  
        return result, totalCount
    
def getById(session, entity):
    result = session.query(entity.__mapper__).get(entity.id)
    if result is None:
        raise BstNoSuchEntityError('No entity of type [{0}] with id [{1}] found.'.format(entity.__mapper__, entity.id))
    return result
     
def create(entity):
    logger.debug('create called')
    
    if entity.id == 0:
        del(entity.id)
    
    if entity.id is not None:
        raise BstTechnicalError('Entity of type [{0}] contains not empty id field with value [{1}]'.format(entity.__mapper__, entity.id))    
    
    with session_scope() as session:

        logger.debug('add entity')
        session.add(entity)
        logger.debug('flush session')
        session.flush()
        #To get the data inserted by INSERT Triggers, we need a refresh 
        logger.debug('refresh entity')
        session.refresh(entity)
        return entity
    
def delete(entity):
    logger.debug('delete called')
    with session_scope() as session:
        session.delete(getById(session, entity))
        return entity
        

        