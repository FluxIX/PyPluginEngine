from .commands import get_registered_commands

def main( args = None ) -> int:
    """
    Executes the given arguments through all of the registered commands.

    There are two registered and one disabled commands in the same directory; a child directory is ignored when discovering modules.
    """

    if args is None:
        args = [ 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, ]

    registered_commands = get_registered_commands()

    output_to_stdout = True
    output_to_stderr = False

    try:
        for name in registered_commands:
            command_type = registered_commands[ name ]
            command = command_type( stdout = output_to_stdout, stderr = output_to_stderr )
            command.execute( *args )
    except Exception as e:
        print( f"Error executing commands: { e }" )
        error_code = 1
    else:
        error_code = 0

    return error_code
