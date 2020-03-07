from typing import Callable
from cli.scripts.utility import CLI
from cli.scripts.config import Properties

cli = CLI(Properties())

def __default_exception_handler(e: Exception):
    cli.debug(f"Not handling exception [{e.__str__()}]")
    raise e

def exception_handler(target: Exception=Exception, handler:Callable[[Exception],None]=__default_exception_handler):
    assert callable(handler)
    def decorator_for_function(func):
        def function_wrapper(*args,**kwargs):
            try:
                return func(*args,**kwargs)
            except Exception as e:
                if type(e) == target:
                    cli.debug(f"Handling exception [{e.__str__()}]")
                    handler(e)
                else:
                    __default_exception_handler(e)
        return function_wrapper
    return decorator_for_function