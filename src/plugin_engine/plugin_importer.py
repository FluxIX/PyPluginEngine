__version__ = r"1.0.0"

from types import ModuleType
from typing import Any, Dict, Tuple

import importlib
from pathlib import Path
from .dynamic_import import import_modules

class PluginImporter( object ):
    """
    Imports plugins dynamically. A plugin is a module relative to a given package.
    """

    def __init__( self, relative_import_package: ModuleType, **kwargs: Dict[ str, Any ] ):
        if not isinstance( relative_import_package, ModuleType ):
            raise ValueError( "The relative import package must a package or module." )

        self._relative_import_package = relative_import_package
        self._loaded_modules = None

    def __del__( self ):
        del self._loaded_modules

    @property
    def relative_import_package( self ) -> ModuleType:
        """
        The package to use as an anchor for imports.
        """

        return self._relative_import_package

    @property
    def _package_directory_path( self ) -> Path:
        """
        The path to search in for modules to load.
        """

        return Path( self.relative_import_package.__file__ ).parent

    @property
    def loaded_modules( self ) -> Tuple[ ModuleType ]:
        """
        The collection of modules previously loaded.
        
        Returns:
        Iterable of modules which are loaded.
        """

        return self._loaded_modules

    @property
    def has_loaded_modules( self ) -> bool:
        """
        Indicates if modules have been loaded on this importer yet.
        
        Returns:
        `True` if modules are currently loaded, `False` otherwise.
        """

        return self.loaded_modules is not None

    def import_modules( self, **kwargs: Dict[ str, Any ] ) -> Tuple[ ModuleType ]:
        """
        Loads modules as relative imports to the relative import package. Files starting '.' will be skipped.
        
        Returns:
        Iterable of modules which were loaded.
        """

        module_file_ext = kwargs.get( "module_file_ext", None )
        if module_file_ext is None:
            module_file_ext = [ ".py" ]

        if not self.has_loaded_modules:
            keyword_args: Dict[ str, Any ] = kwargs.copy()
            keyword_args[ "relative_import_package" ] = self.relative_import_package

            self._loaded_modules = tuple( import_modules( self._package_directory_path, *module_file_ext, **keyword_args ) )

            return self.loaded_modules
        else:
            raise Exception( "Cannot load modules; modules were already loaded." )

    def reload_modules( self ) -> Tuple[ ModuleType ]:
        """
        Reloads modules previously loaded.
        
        Returns:
        Iterable of modules which are loaded.
        """

        self._loaded_modules = tuple( [ importlib.reload( module ) for module in self.loaded_modules ] )

        return self.loaded_modules
