'''
Created on 27.08.2015

@author: oexlt
'''

import logging
from sqlalchemy.sql import or_

logger = logging.getLogger(__name__)


class AbstractFilterParser(object):

    def getOperatorAndValue(self, column, operator, value):
        def like():
            return column.ilike('%' + value + '%')
        def eq():
            return column == value
        def gt():
            return column > value
        def lt():
            return column < value
        switch = {"like": like, "eq": eq, "gt": gt, "lt": lt}
              
        return switch[operator]()
    
    def parseFilter(self, entity, filters):
        raise NotImplementedError('Implement parseFilter in your custom filter class.')
    
class OrLikeTextFilterParser(AbstractFilterParser):
   
    def parseFilter(self, entity, filters):
        orFilterList = list()
        for filter in filters:
            property = filter['property']
            value = filter['value']            
            
            parts = property.lower().split(':')
            
            if len(parts) == 2:
                orFilterList.append(self.getOperatorAndValue(getattr(entity, parts[1]), parts[0], value))
                
            if len(parts) == 3:
                if(parts[0] != 'or'):
                    raise NotImplementedError('filter operation ' + parts[0] + ' is not supported.')
                orFilterList.append(self.getOperatorAndValue(getattr(entity, parts[2]), parts[1], value))                 

        return or_(*orFilterList)

