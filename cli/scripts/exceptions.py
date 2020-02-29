from typing import Callable
import cli.scripts.context as global_context

def __default_exception_handler(e: Exception):
    global_context.debug(f"Not handling exception [{e.__str__()}]")
    raise e

def exception_handler(target: Exception=Exception, handler:Callable[[Exception],None]=__default_exception_handler):
    assert callable(handler)
    def decorator_for_function(func):
        def function_wrapper(*args,**kwargs):
            try:
                return func(*args,**kwargs)
            except Exception as e:
                if type(e) == target:
                    handler(e)
                else:
                    __default_exception_handler(e)
        return function_wrapper
    return decorator_for_function