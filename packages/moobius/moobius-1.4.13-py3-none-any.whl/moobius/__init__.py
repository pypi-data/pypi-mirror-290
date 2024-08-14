# __init__.py

import importlib

for mname in ['moobius.core.sdk', 'core.sdk']:
    try:
        m = importlib.import_module(mname)
        print("Module found:", mname, m)
    except Exception as e:
        print("Module not found:", mname, e)

#from moobius.core import sdk as moobius
from moobius.core.sdk import Moobius
from moobius.core.wand import MoobiusWand
from moobius.database.storage import MoobiusStorage
#from moobius import types as Moobius

import sys
if sys.argv[0] == '-m': # Quickstart option.
    from . import quickstart
    quickstart.save_starter_ccs()
