# Adapted from https://docs.python-guide.org/writing/structure/
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ekaterina.readers import ods_reader
from ekaterina.utils import fsutils
from ekaterina import classes
from ekaterina.utils import gnucash_laska
