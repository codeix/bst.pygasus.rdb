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
from bst.pygasus.core.exc import BstTechnicalError

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
#         import pdb;pdb.set_trace()
        result = (session.query(entityClass)
                  .filter(parser.parseFilter(entityClass, filters))
                  .order_by(*helper.getOrderBy(entityClass, sorters, entityClass.id.asc()))
                  .limit(limit)
                  .offset(start))
                      
        totalCount = session.query(func.count(entityClass.id)).scalar()
  
        return result, totalCount
    
def getById(entity):
    with session_scope() as session:
        session.query(entity.__mapper__).get(entity.id)
        
def reloadEntity(session, entity):
    session.expire(entity)
    return session.query(entity.__mapper__).get(entity.id)
    
def create(entity):
    logger.debug('create called')
    
    if entity.id == 0:
        del(entity.id)
    
    if entity.id is not None:
        raise BstTechnicalError('Entity of type {0} contains not empty id field with value {1}'.format(entity.__mapper__, entity.id))    
    
    with session_scope() as session:


        session.add(entity)
        session.flush()
        #To get the data inserted by INSERT Triggers, we need a reload 
        return reloadEntity(session, entity)
        