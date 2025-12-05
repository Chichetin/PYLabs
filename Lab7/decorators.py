import sys
from functools import wraps
import logging
from typing import Union, Any, Callable

HandleType = Union[Any, logging.Logger]


def logger(func: Callable = None, *, handle: HandleType = sys.stdout) -> Callable:
    """Декоратор для логирования вызовов функций.

    Args:
        func: Функция для декорирования
        handle: Куда писать логи (sys.stdout, io.StringIO, logging.Logger)

    Returns:
        Обернутую функцию с логированием
    """
    if func is None:
        def decorator(actual_func) -> Callable:
            return logger(actual_func, handle=handle)

        return decorator

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        use_logging_module = isinstance(handle, logging.Logger)
        start_message = f"Starting function '{func.__name__}' with args={args}, kwargs={kwargs}"

        if use_logging_module:
            handle.info(start_message)
        else:
            handle.write(f"INFO: {start_message}\n")
            handle.flush()

        try:
            result = func(*args, **kwargs)

            if isinstance(result, tuple) and len(result) == 2:
                actual_result, log_level = result
                success_message = f"Function '{func.__name__}' returned: {actual_result}"

                if use_logging_module:
                    if log_level == logging.INFO:
                        handle.info(success_message)
                    elif log_level == logging.WARNING:
                        handle.warning(success_message)
                    elif log_level == logging.CRITICAL:
                        handle.critical(success_message)
                    else:
                        handle.info(success_message)
                else:
                    level_name = logging.getLevelName(log_level)
                    handle.write(f"{level_name}: {success_message}\n")
                    if hasattr(handle, 'flush'):
                        handle.flush()

                return actual_result
            else:
                success_message = f"Function '{func.__name__}' returned: {result}"
                if use_logging_module:
                    handle.info(success_message)
                else:
                    handle.write(f"INFO: {success_message}\n")
                    if hasattr(handle, 'flush'):
                        handle.flush()
                return result

        except Exception as e:
            error_level = logging.ERROR

            error_message = f"Function '{func.__name__}' raised {type(e).__name__}: {str(e)}"

            if use_logging_module:
                handle.log(error_level, error_message)
            else:
                handle.write(f"{logging.getLevelName(error_level)}: {error_message}\n")
                if hasattr(handle, 'flush'):
                    handle.flush()

            raise


    return wrapper
