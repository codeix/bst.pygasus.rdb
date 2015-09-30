'''
Created on 27.08.2015

@author: oexlt
'''

import logging
from bst.pygasus.rdb import session_scope
from bst.pygasus.rdb import dumpStatement
from sqlalchemy import func

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
    

def getAllPaged(entity, start, limit, sorters, filters, parser):
    logger.debug('getAllPaged called')
    
    helper = QueryHelper()
             
    with session_scope() as session:
        result = (session.query(entity)
                  .filter(parser.parseFilter(entity, filters))
                  .order_by(*helper.getOrderBy(entity, sorters, entity.id.asc()))
                  .limit(limit)
                  .offset(start))
                   
        dumpStatement(result);     
        totalCount = session.query(func.count(entity.id)).scalar()
  
        return result, totalCount