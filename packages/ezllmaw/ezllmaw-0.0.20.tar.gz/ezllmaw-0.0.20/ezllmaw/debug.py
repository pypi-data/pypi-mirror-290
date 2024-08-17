import functools
import ezllmaw as ez

def debug(func, *args, **kwargs):
    @functools(func)
    def wrapper(*args, **kwargs):
        if ez.settings.debug == True:
            return func(*args, **kwargs)
    return wrapper

@debug
def ez_print(*args, **kwargs)->None:
    """Here is vanilla print."""
    print(*args, **kwargs)