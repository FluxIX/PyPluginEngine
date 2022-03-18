from typing import Any, Dict, Iterable

class Command( object ):
    """
    Represents a parent executable command.
    """

    def __init__( self, **kwargs: Dict[ str, Any ] ):
        pass

    def get_name( self ) -> str:
        """
        Gets the name of the command
        """

        raise NotImplementedError( "Child must implement." )

    def execute( self, *args: Iterable[ Any ], **kwargs: Dict[ str, Any ] ) -> bool:
        """
        Executes the command using the given positional and keyword arguments.
        
        Returns:
        `True` if further command execution should continue, `False` otherwise.
        """

        raise NotImplementedError( "Child must implement." )
