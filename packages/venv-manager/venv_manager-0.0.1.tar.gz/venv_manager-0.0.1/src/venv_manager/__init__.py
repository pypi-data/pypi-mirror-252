import sys
from . import main


def in_venv():
    return sys.prefix != sys.base_prefix


if not in_venv():
    print("Hello, please use virtual environment!\n\nTo create virtual environment, use:\n\t`python -m venv venv`")
    exit()
else:
    main.remove_venv()
