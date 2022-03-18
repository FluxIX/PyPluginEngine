from typing import Any, Dict, Iterable

import sys
from . import register_command
from ..command import Command

# The use of the `enabled` keyword argument here is unnecessary, but is here to demonstrate its use.
@register_command( enabled = True )
class EchoCommand( Command ):
    """
    Represents a executable command to print a message .
    """

    def __init__( self, **kwargs: Dict[ str, Any ] ):
        """
        Keyword Arguments:
        `stdout`: if and only if `True` the message is written out to standard output; defaults to `True`.
        `stderr`: if and only if `True` the message is written out to standard error; defaults to `False`.
        """

        self.to_stdout = bool( kwargs.get( "stdout", True ) )
        self.to_stderr = bool( kwargs.get( "stderr", False ) )

    def get_name( self ) -> str:
        """
        Gets the name of the command
        """

        return "echo"

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
