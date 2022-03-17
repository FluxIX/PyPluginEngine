__version__ = r"1.0.0"

from typing import Any, Callable, Dict, Iterable, Type

def register_class( class_ : Type, registration_target : Dict[ Any, Type ], *acceptable_parent_classes : Iterable[ Type ], **kwargs : Dict[ str, Any ] ) -> bool:
    """
    Registers into the given registration target if the given class is a subclass of at least one of the given acceptable parent classes.

    Optional Keyword Arguments:
        `enabled`: boolean which controls if the class should be registered; defaults to `True`.
        `registration_id_extractor_callback`: callable used to extract a registration target-unique ID from the given class. If no callback is provided, the qualified class name is used.
        `quiet_ancestory_mismatch`: boolean which controls if a failed subclass check should result in a raised `Exception`; `True` results in no raised `Exception`, `False` results in a raised `Exception`; defaults to raising an `Exception`.
        `registration_target_lock`: lock controlling access to the registration target; defaults to None, indicating there is lock.

    Returns:
        `True` if the given class was registered, `False` otherwise.

    Notes:
        - If no acceptable parent classes are provided, registration is attempted.
    """

    enabled : bool = bool( kwargs.get( "enabled", True ) )
    result : bool = enabled

    if enabled:
        registration_id_extractor_callback : Callable = kwargs.get( "registration_id_extractor_callback", None )
        if registration_id_extractor_callback is None:
            registration_id_extractor_callback = lambda cls: cls.__qualname__

        if class_ is None:
            raise ValueError( "Class to register cannot be None." )
        elif registration_target is None:
            raise ValueError( "Registration target dictionary cannot be None." )
        else:
            quiet_ancestory_mismatch : bool = bool( kwargs.get( "quiet_ancestory_mismatch", None ) )

            result = len( acceptable_parent_classes ) == 0 or issubclass( class_, acceptable_parent_classes )
            if result:
                lock = kwargs.get( "registration_target_lock", None )
                
                class_id = registration_id_extractor_callback( class_ )

                if lock is not None:
                    lock.acquire( blocking = True )

                try:
                    if class_id not in registration_target:
                        registration_target[ class_id ] = class_
                    else:
                        raise ValueError( f"A class with ID ('{ class_id }') already exists in the registration target." )
                finally:
                    if lock is not None:
                        lock.release()
            elif not quiet_ancestory_mismatch:
                raise ValueError( f"'{ class_.__qualname__ }' class does not have an acceptable parent class." )

    return result
