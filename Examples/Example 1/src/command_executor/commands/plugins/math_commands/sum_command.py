from typing import Any, Dict, Iterable, List

import sys
from .. import register_command
from ...command import Command

@register_command()
class SumCommand( Command ):
    """
    Represents a executable command to print the sum of the arguments.
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

        return "sum"

    def execute( self, *args: Iterable[ Any ], **kwargs: Dict[ str, Any ] ) -> bool:
        """
        Executes the command using the given positional and keyword arguments.
        
        Returns:
        `True` if further command execution should continue, `False` otherwise.
        """

        arguments: List[ int ] = [ int( arg ) for arg in args ]
        sum_ = sum( arguments )

        if self.to_stdout:
            print( sum_, file = sys.stdout )

        if self.to_stderr:
            print( sum_, file = sys.stderr )

        return False
