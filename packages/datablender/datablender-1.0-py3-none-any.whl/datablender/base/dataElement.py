"""

"""
from typing import List, Union, Dict

import os
import copy

from datablender.base.connection import Connection,AsyncConnection
from datablender.base.dataLogging import DataLogging,AsyncDataLogging
from datablender.base.dataConfiguration import DataConfiguration,AsyncDataConfiguration
from datablender.base.queryBuilder import QueryBuilder
from datablender.base.file import File

class DataElement:
    """Represent a data element (data source, table, schema, ...)

    Attributes:
    ----------
        connection (Connection): Connection to a database.
        name (str): Element's name.

    Methods:
    ----------
        Methods

    Examples:
    ----------
        >>> import datablender

    """
    def __init__(
        self,
        connection:Connection,
        name:str,
        element_type:str = 'table',
        status:str = 'default',
        data_configuration:DataConfiguration = None,
        acticvate_data_config:bool = False,
        id:int=None,
        content:list=[],
        event_server=None
    ):
        self.connection = connection
        self.element_type = element_type
        self.name = name
        self.status = status
        self.id = id
        self.content = content
       
        config = File(
            path = os.path.join(
                os.path.dirname(__file__),
                '..',
                'configuration.json'
            )
        ).read().content
        
        self.attributes:List[dict] = config['elements'][self.element_type]['attributes']

        self.data_configuration = data_configuration if data_configuration else DataConfiguration(
            active=acticvate_data_config
        )

        self.data_logging = DataLogging(
            self.connection,
            event_server,
            initiate_table= not(self.element_type == 'extension' and self.name == 'postgis')
        )

        self.query_builder = QueryBuilder(
            self.connection,
            config
        )

        self.manage_from = None
        
    @property
    def config_element(self) -> dict:
    
        return self.data_configuration.getElement(
            self.name,
            self.element_type,
            self.id,
            getattr(self,'schema_id',None)
        )

    def getAttributeValue(
        self,
        attribute_name:str, # owner_id
        database_name:str, # owner
        element_type:str, # role
        source:str
    ) -> None:
        
        if source == 'values':
            return True, getattr(
                self,
                database_name if (
                    not self.data_configuration.active
                    and database_name
                ) else attribute_name
            )
        
        elif source == 'configuration':
            return attribute_name in self.config_element, self.config_element.get(
                attribute_name
            )
        
        elif source == 'database':
            name = database_name if database_name else attribute_name

            db_element:dict = getattr(
                self,
                'db_element'
            )

            if name in db_element:

                return True, self.data_configuration.getElement(
                    db_element.get(name),
                    element_type
                ).get('id') if (
                    self.data_configuration.active and database_name
                ) else db_element.get(name)
        
        return False, None
    
    def setForeignAttribute(
        self,
        name,
        database_name,
        element_type
    ) -> None:
        setattr(
            self,
            database_name if getattr(self,name) else name,
            self.data_configuration.getElement(
                getattr(self,database_name),
                element_type,
                getattr(self,name)
            ).get('name' if getattr(self,name) else 'id')
        )

    def manageAttribute(
        self,
        update:str,
        name:str,
        setter:str = None,
        element_type:str = None,
        database_name:str = None,
        **kwargs
    ) -> Union[None,bool]:
        
        if name == 'size':
            return False
        
        if update:

            value_from_is_comparable, value_from = self.getAttributeValue(
                name,
                database_name,
                element_type,
                self.manage_from
            )
            
            value_to_is_comparable, value_to = self.getAttributeValue(
                name,
                database_name,
                element_type,
                update
            )

            value_not_equal = self.setCompareValue(
                copy.deepcopy(value_from)
            ) != self.setCompareValue(
                copy.deepcopy(value_to)
            )

            if value_not_equal and value_from_is_comparable and value_to_is_comparable:

                if update == 'database':
                    
                    getattr(
                        self,
                        setter
                    )() if setter else None
                    
                else:
                    setattr(
                        self,
                        database_name if database_name else name,
                        copy.deepcopy(value_from)
                    )
                    
                    if database_name:
                        self.setForeignAttribute(
                            name,
                            database_name,
                            element_type
                        )
            
            return value_not_equal if value_from_is_comparable and value_to_is_comparable else False
        
        elif self.data_configuration.active:

            if database_name:
                self.setForeignAttribute(
                    name,
                    database_name,
                    element_type
                )

            elif (
                name in ['name','id']
                and self.element_type != 'database'
                and self.config_element
            ):
                
                attribute_name = 'name' if name == 'id' else 'id'

                setattr(
                    self,
                    attribute_name,
                    self.config_element.get(
                        attribute_name
                    )
                ) if not getattr(self,attribute_name) else None

    def manageAttributes(
        self,
        update:str = None
    ) -> None:
        
        return any([
            self.manageAttribute(
                update,
                **attribute
            )
            for attribute in self.attributes
        ])
 
    def setCompareValue(
        self,
        value:Union[
            List[Dict[str,str]],
            list,
            str
        ]
    ) -> Union[
        List[Dict[str,str]],
        list,
        str
    ]:
        if isinstance(value,list):
            value = [
                self.setCompareValue(sub_value)
                for sub_value in value
            ]
            value.sort(
                key=(
                    lambda x: x.get(
                        'name'
                    ) if x.get('name') else ''.join([
                        x[key] for key in x
                    ])
                ) if all([
                    isinstance(sub_value,dict)
                    for sub_value in value
                ]) else None
            )
    
        elif isinstance(value,dict):
            value= {
                key:self.setCompareValue(value.get(key))
                for key in value
                if value.get(key) # check if None or empty
            } 
        
        return value   

class AsyncDataElement:
    """Represent a data element (data source, table, schema, ...)

    Attributes:
    ----------
        connection (Connection): Connection to a database.
        name (str): Element's name.

    Methods:
    ----------
        Methods

    Examples:
    ----------
        >>> import datablender

    """
    def __init__(
        self,
        connection:AsyncConnection,
        name:str,
        element_type:str = 'table',
        status:str = 'default',
        data_configuration:AsyncDataConfiguration = None,
        acticvate_data_config:bool = False,
        id:int=None,
        content:list=[],
        event_server=None
    ):
        self.connection = connection
        self.element_type = element_type
        self.name = name
        self.status = status
        self.id = id
        self.content = content
       
        config = File(
            path = os.path.join(
                os.path.dirname(__file__),
                '..',
                'configuration.json'
            )
        ).read().content
        
        self.attributes:List[dict] = config['elements'][self.element_type]['attributes']

        self.data_configuration = data_configuration if (
            data_configuration
        ) else AsyncDataConfiguration(
            active=acticvate_data_config
        )

        self.query_builder = QueryBuilder(
            self.connection,
            config
        )

        self.data_logging = AsyncDataLogging(
            self.connection,
            self.element_type,
            event_server
        )

        self.manage_from = None
        
    @property
    def config_element(self) -> dict:
    
        return self.data_configuration.getElement(
            self.name,
            self.element_type,
            self.id,
            getattr(self,'schema_id',None)
        )

    def getAttributeValue(
        self,
        attribute_name:str, # owner_id
        database_name:str, # owner
        element_type:str, # role
        source:str
    ) -> None:
        
        if source == 'values':
            return True, getattr(
                self,
                database_name if (
                    not self.data_configuration.active
                    and database_name
                ) else attribute_name
            )
        
        elif source == 'configuration':
            return attribute_name in self.config_element, self.config_element.get(
                attribute_name
            )
        
        elif source == 'database':
            name = database_name if database_name else attribute_name

            db_element:dict = getattr(
                self,
                'db_element'
            )

            if name in db_element:

                return True, self.data_configuration.getElement(
                    db_element.get(name),
                    element_type
                ).get('id') if (
                    self.data_configuration.active and database_name
                ) else db_element.get(name)
        
        return False, None
    
    async def setForeignAttribute(
        self,
        name,
        database_name,
        element_type
    ) -> None:
        await self.data_configuration.getElements(element_type)
        setattr(
            self,
            database_name if getattr(self,name) else name,
            self.data_configuration.getElement(
                getattr(self,database_name),
                element_type,
                getattr(self,name)
            ).get('name' if getattr(self,name) else 'id')
        )

    async def manageAttribute(
        self,
        update:str,
        name:str,
        setter:str = None,
        element_type:str = None,
        database_name:str = None,
        **kwargs
    ) -> Union[None,bool]:
        
        if name == 'size':
            return False
        
        if update:

            value_from_is_comparable, value_from = self.getAttributeValue(
                name,
                database_name,
                element_type,
                self.manage_from
            )
            
            value_to_is_comparable, value_to = self.getAttributeValue(
                name,
                database_name,
                element_type,
                update
            )

            value_not_equal = self.setCompareValue(
                copy.deepcopy(value_from)
            ) != self.setCompareValue(
                copy.deepcopy(value_to)
            )

            if value_not_equal and value_from_is_comparable and value_to_is_comparable:

                if update == 'database':
                    
                    await getattr(
                        self,
                        setter
                    )() if setter else None
                    
                else:
                    setattr(
                        self,
                        database_name if database_name else name,
                        copy.deepcopy(value_from)
                    )
                    
                    if database_name:
                        await self.setForeignAttribute(
                            name,
                            database_name,
                            element_type
                        )
            
            return value_not_equal if value_from_is_comparable and value_to_is_comparable else False
        
        elif self.data_configuration.active:

            if database_name:
                await self.setForeignAttribute(
                    name,
                    database_name,
                    element_type
                )

            elif (
                name in ['name','id']
                and self.element_type != 'database'
                and self.config_element
            ):
                
                attribute_name = 'name' if name == 'id' else 'id'

                setattr(
                    self,
                    attribute_name,
                    self.config_element.get(
                        attribute_name
                    )
                ) if not getattr(self,attribute_name) else None

    async def manageAttributes(
        self,
        update:str = None
    ) -> None:
        
        return any([
            await self.manageAttribute(
                update,
                **attribute
            )
            for attribute in self.attributes
        ])
 
    def setCompareValue(
        self,
        value:Union[
            List[Dict[str,str]],
            list,
            str
        ]
    ) -> Union[
        List[Dict[str,str]],
        list,
        str
    ]:
        if isinstance(value,list):
            value = [
                self.setCompareValue(sub_value)
                for sub_value in value
            ]
            value.sort(
                key=(
                    lambda x: x.get(
                        'name'
                    ) if x.get('name') else ''.join([
                        x[key] for key in x
                    ])
                ) if all([
                    isinstance(sub_value,dict)
                    for sub_value in value
                ]) else None
            )
    
        elif isinstance(value,dict):
            value= {
                key:self.setCompareValue(value.get(key))
                for key in value
                if value.get(key) # check if None or empty
            } 
        
        return value   
