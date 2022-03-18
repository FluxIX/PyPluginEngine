import sys
from .main import main as entry_point

if __name__ == "__main__":
    script_name = sys.argv[ 0 ]

    sys.exit( entry_point() )
