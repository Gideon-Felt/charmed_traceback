from .colored_traceback import add_hook, Charmify

"""
# Example Usage
# Using a method such as this ensures that this Library isn't a strict dependency and can gently be removed,
# or only present as a developer dependency.

import contextlib

def call_dev_charm_colorize_traceback() -> None:
    with contextlib.suppress(ImportError):
        import colored_traceback.auto
        colored_traceback.add_hook()

call_dev_charm_colorize_traceback()

def test_to_failure():
    while True:
        raise FileNotFoundError


test_to_failure()
"""