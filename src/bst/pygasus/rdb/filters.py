'''
Created on 27.08.2015

@author: oexlt
'''

import logging
from sqlalchemy.sql import or_
from sqlalchemy.sql import and_

logger = logging.getLogger(__name__)


class AbstractFilterParser(object):

    def createOperation(self, column, operator, value):
        def like():
            return column.ilike('%' + value + '%')
        def eq():
            return column == value
        def gt():
            return column > value
        def lt():
            return column < value
        switch = {'like': like, 'eq': eq, 'gt': gt, 'lt': lt}
              
        return switch[operator]()
    
    def parseFilter(self, entity, filters):
        raise NotImplementedError('Implement parseFilter in your custom filter class.')
    
class OrLikeTextFilterParser(AbstractFilterParser):
    '''Parses filters in custom OR:LIKE format used for multi column text searches with iLike operator
    Example:
        filter: [{"property":"LIKE:Log_Num","value":"_2174"},{"property":"OR:LIKE:Description","value":"_2174"}]
        operations: Log_Num ilike '%_2174%' or Description ilike '%_2174%'
    '''   
    def parseFilter(self, entity, filters):
        orFilterList = list()
        for filter in filters:
            property = filter['property']
            value = filter['value']            
            
            parts = property.lower().split(':')
            
            if len(parts) == 2:
                orFilterList.append(self.createOperation(getattr(entity, parts[1]), parts[0], value))
                
            if len(parts) == 3:
                if(parts[0] != 'or'):
                    raise NotImplementedError('filter operation [' + parts[0].upper() + '] is not supported by OrLikeTextFilterParser.')
                orFilterList.append(self.createOperation(getattr(entity, parts[2]), parts[1], value))                 

        return or_(*orFilterList)

class StandardFilterParser(AbstractFilterParser):
    '''
    TODO
    '''
    
    def parseFilter(self, entity, filters):
        filterList = list()
        for filter in filters:
            filterList.append(self.createOperation('1', 'eq', '1'))
        return and_(*filterList)
