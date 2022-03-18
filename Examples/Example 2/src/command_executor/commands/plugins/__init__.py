from typing import Any, Dict, Type

from multiprocessing import RLock
from plugin_engine.class_registration import register_class
from ..command import Command

_lock: RLock = RLock()
_commands: Dict[ str, Type ] = {}

def register_command( **kwargs: Dict[ str, Any ] ):
    """
    Decorator which registers a class as a Command.
    """

    enabled = bool( kwargs.get( "enabled", True ) )

    def class_decorator( cls: Type ):
        register_class( cls, _commands, Command, enabled = enabled, lock = _lock )
        return cls

    return class_decorator
