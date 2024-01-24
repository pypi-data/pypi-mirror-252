""" Main logging hook """


from typing import Any, Callable

import pplog.log_checks as lc
from pplog.config import get_ppconfig


def log_this(key: str, output_check: bool = True) -> Callable:
    """Wrapper function

    Args:
        key (str): ppconf identifier key
        output_check (bool - Optional - defaults to True): whether to log the result
            of the LogCheck on func's output
    """

    def decorator(func) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            config: dict = get_ppconfig()
            params: dict = config[key]
            check_class_str: str = params["log_check_class"]
            check_class_arguments = params["arguments"]
            check_class = getattr(lc, check_class_str)
            # Call the original function
            result = func(*args, **kwargs)
            if output_check:
                log_result = check_class(result, check_class_arguments).check()
                print(log_result)

            return result

        return wrapper

    return decorator
