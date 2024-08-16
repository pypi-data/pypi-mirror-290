"""
This module contains classes to manipulate file system elements, like files, zipfiles and directories.
"""
from __future__ import annotations
from typing import Union

import os
import shutil
import zipfile
import traceback

from datablender.base import getDirectoryElementName

class Directory:
    """Directory class

    Attributes:
    ----------
        Name (str): Name of the directory

    Methods:
    ----------
        Methods
    """
    def __init__(self,name:str):
        """Directory class initialisation
        Args:
            name (str): Directory name
        """
        self.name = name
        if self.name and self.exists:
            self.setName()
        
    def setName(self) -> None:
        self.name = os.path.abspath(self.name)

    @property
    def exists(self):
        """Check if directory exists
        """
        return os.path.isdir(self.name)

    @property
    def elements_name(self):
        """Get elements in directory.
        """
        return os.listdir(self.name)

    @property
    def name_(self):
        """Get the last directory name.
        """
        return os.path.basename(self.name)
    
    def make(self) -> Directory:
        """Make a directory.
        """
        if not self.exists:
            os.makedirs(self.name,exist_ok=True) 
        return self

    def deleteElements(self,ignored_file:str='.keep'):
        """Delete all elements
        Args:
            ignored_file (str, optional): Element to ignore. Defaults to '.keep'.
        """
        
        for element_name in self.elements_name:
            if element_name != ignored_file:
                DirectoryElement(element_name,self.name).delete()

    def delete(self) -> None:
        """Delete directory.
        """
        shutil.rmtree(self.name)

    def join(self,*elements_to_join:str,inplace:bool = True) -> Union[Directory,str]:
        """Join element to directory name.

        Args:
            elements_to_join (str): Elements to join.
            inplace (bool, optional): Inpalce the directory name or return the join name. Defaults to False.

        Returns:
            Union[Directory,str]: If inplace, return self, else return the joined name.
        """
        if inplace:
            self.name = os.path.join(self.name,*elements_to_join)
            return self
        else:
            return os.path.join(self.name,*elements_to_join)
        
    def checkJoinExists(self,*elements_to_join:str) -> bool:
        
        return os.path.isdir(os.path.join(self.name,*elements_to_join))

class DirectoryElement:
    """Element of a directory, which can be a file, directory of a zip file
    Attributes:
        name
    Methods:
        Methods
    """
    def __init__(
        self,
        name:str = None,
        directory_name:str = None,
        path:str = None
    ):
        """Initialization function
        Args:
            name (str): Name of the element
            directory_name (str): Name of the directory
        """
        self.directory_name,self.name = getDirectoryElementName(
            path,
            directory_name,
            name
        )
        self.checkType()

    @property
    def path(self):
        """Set path of the element.
        """
        return os.path.join(self.directory_name, self.name)
    
    @property
    def extension(self):
        """Get the file extension
        """
        return os.path.splitext(self.path)[-1].lower()[1:]

    def checkType(self):
        """Check the element type.
        """
        self.is_directory = os.path.isdir(self.path+'/')
        self.is_file = os.path.isfile(self.path)
        self.is_zip_file = False if self.is_file and self.extension == 'xlsx' else zipfile.is_zipfile(self.path)
        self.is_link = os.path.islink(self.path)
        self.is_temp_file = self.name[:2] == '~$'
    
    def delete(self) -> None:
        """Delete the element.
        """
        try:
            if self.is_file or self.is_link:
                os.unlink(self.path)
            elif self.is_directory:
                shutil.rmtree(self.path)
        except Exception as e:
            'Failed to delete %s. Reason: %s' % (self.path, traceback.format_exc())
