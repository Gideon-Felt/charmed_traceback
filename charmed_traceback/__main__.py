from typing import Any, Dict
import os
import sys
import charmed_traceback

charmed_traceback.add_hook()

# Check that a script was passed in.
if len(sys.argv) <= 1:
    raise SystemExit("Usage: python -m charmed_traceback my_script.py")

# Check that the script exists.
script_path = sys.argv[1]
if not os.path.exists(script_path):
    raise SystemExit("Error: '%s' does not exist" % script_path)

# Replace charmed_traceback's dir with script's dir in the module search path.
sys.path[0] = os.path.dirname(script_path)

# Remove charmed_traceback from the arg list.
del sys.argv[0]

with open(script_path) as script_file:
    code = compile(script_file.read(), script_path, 'exec')
    variables: Dict[Any, Any] = {}
    exec(code, variables, variables)
