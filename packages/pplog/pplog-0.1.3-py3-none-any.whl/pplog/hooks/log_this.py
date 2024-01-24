""" Main logging hook """


from typing import Any, Callable

from pplog.adapter import log_check_to_splunk
from pplog.config import get_class_from_dot_path, get_ppconfig
from pplog.log_checks.check_model import LogCheckResult


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
            check_class = get_class_from_dot_path(check_class_str)
            # Call the original function
            result = func(*args, **kwargs)
            log_result: LogCheckResult = check_class(key, result, check_class_arguments).check()
            if output_check:
                # TODO: fix how this is initialized
                log_check_to_splunk(
                    stage=config.get("stage", "test"),
                    tenant_id=config.get("logging", {}).get("tenant_id", "test"),
                    splunk_event_endpoint=config.get("ppconf", {}).get(
                        "event_grid_topic_endpoint", "testendpoint"
                    ),
                    log_check_result=log_result,
                )

            return result

        return wrapper

    return decorator
