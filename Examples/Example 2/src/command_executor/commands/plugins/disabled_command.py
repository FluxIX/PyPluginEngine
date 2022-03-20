from typing import Any, Dict, Iterable

import sys
from . import register_command
from ..command import Command

@register_command( enabled = False )
class DisabledCommand( Command ):
    """
    Represents a executable command to print a message .
    """

    def __init__( self, **kwargs: Dict[ str, Any ] ):
        self.to_stdout = bool( kwargs.get( "stdout", True ) )
        self.to_stderr = bool( kwargs.get( "stderr", False ) )

    def get_name( self ) -> str:
        """
        Gets the name of the command
        """

        return "disabled"

    def execute( self, *args: Iterable[ Any ], **kwargs: Dict[ str, Any ] ) -> bool:
        """
        Executes the command using the given positional and keyword arguments.
        
        Returns:
        `True` if further command execution should continue, `False` otherwise.
        """

        if self.to_stdout:
            print( args, file = sys.stdout )

        if self.to_stderr:
            print( args, file = sys.stderr )

        return True
