__version__ = r"1.0.0"

from types import ModuleType
from typing import Any, Dict, Iterable, List, Set, Union

import importlib
import os
import os.path
from pathlib import Path

def import_modules( directory_path: Union[ str, Path ], *target_file_extensions: Iterable[ str ], **kwargs: Dict[ str, Any ] ) -> List[ ModuleType ]:
    """
    Imports modules from files from the given directory path which have one of the target file extensions. Modules whose filenames start with a period are ignored.

    Parameters:
    `directory_path`: directory path to load modules from.
    `target_file_extensions`: iterable of file extensions to match file to load from.

    Keywords:
    `relative_import_package`: package the modules are imported relative to; defaults to None indicating the imports are absolute.
    `recursive`: indicates if the directory path should be searched recursively; defaults to `False`..
    `ignored_filenames`: iterable of filenames which are ignored when discovering modules to import.

    Returns:
    List of modules loaded.

    Notes:
        - If the directory path is a relative string, it is assumed to be relative from the current working directory.
    """

    if isinstance( directory_path, str ):
        if not os.path.isabs( directory_path ):
            directory_path: Path = Path( os.getcwd(), directory_path )
        else:
            directory_path: Path = Path( directory_path )
    elif not isinstance( directory_path, Path ):
        raise ValueError( "Directory path must be a Path instance." )

    relative_import_package_name: ModuleType = kwargs.get( "relative_import_package", None )
    if relative_import_package_name is not None:
        if isinstance( relative_import_package_name, ModuleType ):
            relative_import_package_name = relative_import_package_name.__name__
        elif not isinstance( relative_import_package_name, str ):
            raise ValueError( f"Invalid relative import package name: { relative_import_package_name }" )

    recursive: bool = bool( kwargs.get( "recursive", False ) )

    raw_ignored_filenames: Iterable[ Union[ str, Path ] ] = kwargs.get( "ignored_filenames", None )
    if raw_ignored_filenames is None:
        raw_ignored_filenames = [ "__init__", "__main__" ]

    ignored_filenames: Set[ Path ] = set()
    for filename in raw_ignored_filenames:
        if isinstance( filename, str ):
            filename = Path( filename )
        elif not isinstance( filename, Path ):
            raise ValueError( "Invalid ignored filename; filename must be a Path." )

        ignored_filenames.add( filename )
    _ignored_filenames = set( map( lambda x: x.stem, ignored_filenames ) )

    # verify the target_file_extensions
    for ext in target_file_extensions:
        if not isinstance( ext, str ):
            raise ValueError( f"File extension '{ ext }' is not a valid string." )

    modules_imported: List[ ModuleType ] = []

    for root, directories, filenames in os.walk( directory_path, topdown = True ):
        if not recursive:
            directories[:] = []

        failed_imports = []

        if directory_path != root:
            subdirectories = Path( os.path.relpath( root, directory_path ) ).parts
            additional_pathage_path = "".join( map( lambda x: f"{ x }.", subdirectories ) )
        else:
            additional_pathage_path = ""

        for filename in filenames:
            name, extension = os.path.splitext( filename )

            if extension in target_file_extensions and not name.lstrip().startswith( "." ) and name not in _ignored_filenames:
                module_name = f".{ additional_pathage_path }{ name }"

                try:
                    imported_module = importlib.import_module( module_name, relative_import_package_name )
                except ImportError as e:
                    failed_imports.append( ( module_name, filename, root, e ) )
                else:
                    modules_imported.append( imported_module )

        last_failed_import_count = None
        # while there are failed imports and the last iteration resolved some of the previously-failed imports.
        while len( failed_imports ) > 0 and ( last_failed_import_count is None or last_failed_import_count > len( failed_imports ) ):
            last_failed_import_count = len( failed_imports )

            module_index = 0
            while module_index < len( failed_imports ):
                module_name, filename, _, _ = failed_imports[ module_index ]

                try:
                    imported_module = importlib.import_module( module_name, relative_import_package_name )
                except ImportError:
                    module_index += 1
                else:
                    failed_imports.pop( module_index )
                    modules_imported.append( imported_module )

        if len( failed_imports ) > 0:
            raise ImportError( f"Unable to dynamically import the following modules from the '{ root }' directory: { ', '.join( map( lambda m: m[ 0 ], failed_imports ) ) }" )

    if len( modules_imported ) > 0:
        importlib.invalidate_caches()

    return modules_imported
