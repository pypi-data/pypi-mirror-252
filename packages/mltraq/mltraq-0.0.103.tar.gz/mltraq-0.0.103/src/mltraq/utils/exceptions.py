import inspect
import sys
import traceback

from mltraq import options


def exception_message():
    if options.get("execution.exceptions.compact_message"):
        return compact_exception_message()
    else:
        return complete_exception_message()


def complete_exception_message():
    return traceback.format_exc()


def compact_exception_message():
    """Construct string representing , in a compact way, the traceback, useful to handle exceptions.

    Args:
        e (_type_): Raised exception.

    Returns:
        _type_: _description_
    """

    exc_type, exc_value, exc_traceback = sys.exc_info()
    frame = inspect.trace()[-1]

    details = {
        "file": exc_traceback.tb_frame.f_code.co_filename,
        "lineno": exc_traceback.tb_lineno,
        "type": exc_type.__name__,
        "message": str(exc_value),
        "trace": f'{frame.filename}:{frame.lineno}::{frame.function} "{frame.code_context[frame.index].strip()}"',
    }

    return f'{details["type"]} at {details["trace"]}: {details["message"]}'
