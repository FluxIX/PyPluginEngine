# Cannot use a relative import here.
from command_executor.main import main as entry_point

if __name__ == '__main__':
    import sys
    ret_value = entry_point()

    sys.exit( ret_value )
