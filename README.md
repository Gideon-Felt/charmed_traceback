# Charmed Traceback
JetBrains style Tracebacks everywhere.<br>
Automatically apply traceback styling akin to Jetbrains Traceback highlighting, providing much easier debugging and log searching, as-well as feel more at home away from PyCharm


# Installation
### Through pip:<br>
`pip install charmed-traceback`
### Build with poetry:<br>
`pip install Poetry`<br>
`poetry build`

# Usage
### Charmed Traceback can be executed as a module:
`python -m charmed_traceback somefile.py`
### Charmed Traceback also works well within a script or even directly in the interpreter REPL. Standard usage will re-stylize the output, unless it's being redirected to a pipe:
```python
import charmed_traceback
charmed_traceback.add_hook()
```
### If want to retain the charmed style even when stderr is being piped, tack on an always=True argument:
```python
import charmed_traceback
charmed_traceback.add_hook(always=True)
```
### There are also a couple of convenience imports, which get the footprint down to one line:
```python
# Same as add_hook()
import charmed_traceback.auto

# Same as add_hook(always=True)
import charmed_traceback.always
```
### When implementing with a project that alternates between having access to development dependencies and not having those dependencies, it would be most convenient to provide a context manager to use this Charmed Tracebacks:
```python
import contextlib

def dev_charm_traceback_handler() -> None:
    with contextlib.suppress(ImportError):
        import charmed_traceback.auto

# This call can be left in a project regaurdless of the presence of Charmed Traceback package.
dev_charm_traceback_handler()
```