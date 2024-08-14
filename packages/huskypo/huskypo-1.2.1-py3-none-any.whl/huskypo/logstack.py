# Author: Johnny Chou
# Email: johnny071531@gmail.com
# PyPI: https://pypi.org/project/huskypo/
# GitHub: https://github.com/uujohnnyuu/huskyPO

# If you want to reference this logstack method to construct your own model or extend it,
# you must understand the following points; otherwise, unexpected errors may occur.

# 1. We must ensure that the stack level of "get_stack_info" and "logging" are consistent
#       in order to use the level found by get_stack_info for logging.
# 2. This is why we do not encapsulate the calculation of target_level
#       into a function in each logging function.


from __future__ import annotations

import inspect
import logging
import os
from typing import Mapping

from .config import Log


def debug(
    message: object,
    starts_with: str = 'test',
    stack_adjust: int = 0,
    exc_info: bool | tuple | None = None,
    stack_info: bool = False,
    stack_level: int | None = None,
    extra: Mapping[str, object] | None = None
) -> None:
    """
    Calling `logging.debug` method, and finding stacklevel starts with specific function name.

    - message: The message format string, or an object to be logged.
        If it is an object, it is converted to a string using str().
    - starts_with: Records the log information in the function or module name that starts with the starts_with keyword.
        For example, `'test'` means the log will be displayed in the function `test_xxx()` or the module `test_xxx.py`.
        If both a module and a function have the same prefix, the function takes precedence.
        If the target is not found, it defaults to the first caller of this `logstack`.
    - stack_adjust: Adjusts the base frame to reduce unnecessary frame queries.
        For instance, `stack_adjust = 0` means no adjustment is made, and the search starts from the next layer by default;
        `stack_adjust = 2` means the search starts from three layers down by default.
    - exc_info: If True, exception information is added to the logging message.
        If an exception tuple (in the format returned by sys.exc_info()) is provided, it is used.
        Default is None, which means no exception information is added.
    - stack_info: If True, stack information is added to the logging message.
    - stack_level: If provided, specifies which stack frame to use when logging the call.
        Default is 1, which means the immediate caller's frame.
    - extra: A dictionary of extra context to be added to the logging message.
        This can be used to pass additional information that can be used by the logging handlers.
        For example: extra={'user': 'Johnnny'}
    """
    target_level = get_stack_level(starts_with, stack_adjust + 1) if stack_level is None else stack_level + 1
    logging.debug(message, exc_info=exc_info, stack_info=stack_info, stacklevel=target_level, extra=extra)


def info(
    message: str,
    starts_with: str = 'test',
    stack_adjust: int = 0,
    exc_info: bool | tuple | None = None,
    stack_info: bool = False,
    stack_level: int | None = None,
    extra: Mapping[str, object] | None = None
) -> None:
    """
    Calling logging.info method, and finding stacklevel starts with specific function name.

    - message: The message format string, or an object to be logged.
        If it is an object, it is converted to a string using str().
    - starts_with: Records the log information in the function or module name that starts with the starts_with keyword.
        For example, `'test'` means the log will be displayed in the function `test_xxx()` or the module `test_xxx.py`.
        If both a module and a function have the same prefix, the function takes precedence.
        If the target is not found, it defaults to the first caller of this `logstack`.
    - stack_adjust: Adjusts the base frame to reduce unnecessary frame queries.
        For instance, `stack_adjust = 0` means no adjustment is made, and the search starts from the next layer by default;
        `stack_adjust = 2` means the search starts from three layers down by default.
    - exc_info: If True, exception information is added to the logging message.
        If an exception tuple (in the format returned by sys.exc_info()) is provided, it is used.
        Default is None, which means no exception information is added.
    - stack_info: If True, stack information is added to the logging message.
    - stack_level: If provided, specifies which stack frame to use when logging the call.
        Default is 1, which means the immediate caller's frame.
    - extra: A dictionary of extra context to be added to the logging message.
        This can be used to pass additional information that can be used by the logging handlers.
        For example: extra={'user': 'Johnnny'}
    """
    target_level = get_stack_level(starts_with, stack_adjust + 1) if stack_level is None else stack_level + 1
    logging.info(message, exc_info=exc_info, stack_info=stack_info, stacklevel=target_level, extra=extra)


def warning(
    message: str,
    starts_with: str = 'test',
    stack_adjust: int = 0,
    exc_info: bool | tuple | None = None,
    stack_info: bool = False,
    stack_level: int | None = None,
    extra: Mapping[str, object] | None = None
) -> None:
    """
    Calling logging.warning method, and finding stacklevel starts with specific function name.

    - message: The message format string, or an object to be logged.
        If it is an object, it is converted to a string using str().
    - starts_with: Records the log information in the function or module name that starts with the starts_with keyword.
        For example, `'test'` means the log will be displayed in the function `test_xxx()` or the module `test_xxx.py`.
        If both a module and a function have the same prefix, the function takes precedence.
        If the target is not found, it defaults to the first caller of this `logstack`.
    - stack_adjust: Adjusts the base frame to reduce unnecessary frame queries.
        For instance, `stack_adjust = 0` means no adjustment is made, and the search starts from the next layer by default;
        `stack_adjust = 2` means the search starts from three layers down by default.
    - exc_info: If True, exception information is added to the logging message.
        If an exception tuple (in the format returned by sys.exc_info()) is provided, it is used.
        Default is None, which means no exception information is added.
    - stack_info: If True, stack information is added to the logging message.
    - stack_level: If provided, specifies which stack frame to use when logging the call.
        Default is 1, which means the immediate caller's frame.
    - extra: A dictionary of extra context to be added to the logging message.
        This can be used to pass additional information that can be used by the logging handlers.
        For example: extra={'user': 'Johnnny'}
    """
    target_level = get_stack_level(starts_with, stack_adjust + 1) if stack_level is None else stack_level + 1
    logging.warning(message, exc_info=exc_info, stack_info=stack_info, stacklevel=target_level, extra=extra)


def error(
    message: str,
    starts_with: str = 'test',
    stack_adjust: int = 0,
    exc_info: bool | tuple | None = None,
    stack_info: bool = False,
    stack_level: int | None = None,
    extra: Mapping[str, object] | None = None
) -> None:
    """
    Calling logging.error method, and finding stacklevel starts with specific function name.

    - message: The message format string, or an object to be logged.
        If it is an object, it is converted to a string using str().
    - starts_with: Records the log information in the function or module name that starts with the starts_with keyword.
        For example, `'test'` means the log will be displayed in the function `test_xxx()` or the module `test_xxx.py`.
        If both a module and a function have the same prefix, the function takes precedence.
        If the target is not found, it defaults to the first caller of this `logstack`.
    - stack_adjust: Adjusts the base frame to reduce unnecessary frame queries.
        For instance, `stack_adjust = 0` means no adjustment is made, and the search starts from the next layer by default;
        `stack_adjust = 2` means the search starts from three layers down by default.
    - exc_info: If True, exception information is added to the logging message.
        If an exception tuple (in the format returned by sys.exc_info()) is provided, it is used.
        Default is None, which means no exception information is added.
    - stack_info: If True, stack information is added to the logging message.
    - stack_level: If provided, specifies which stack frame to use when logging the call.
        Default is 1, which means the immediate caller's frame.
    - extra: A dictionary of extra context to be added to the logging message.
        This can be used to pass additional information that can be used by the logging handlers.
        For example: extra={'user': 'Johnnny'}
    """
    target_level = get_stack_level(starts_with, stack_adjust + 1) if stack_level is None else stack_level + 1
    logging.error(message, exc_info=exc_info, stack_info=stack_info, stacklevel=target_level, extra=extra)


def exception(
    message: str,
    starts_with: str = 'test',
    stack_adjust: int = 0,
    exc_info: bool | tuple | None = True,
    stack_info: bool = False,
    stack_level: int | None = None,
    extra: Mapping[str, object] | None = None
) -> None:
    """
    Calling logging.exception method, and finding stacklevel starts with specific function name.

    - message: The message format string, or an object to be logged.
        If it is an object, it is converted to a string using str().
    - starts_with: Records the log information in the function or module name that starts with the starts_with keyword.
        For example, `'test'` means the log will be displayed in the function `test_xxx()` or the module `test_xxx.py`.
        If both a module and a function have the same prefix, the function takes precedence.
        If the target is not found, it defaults to the first caller of this `logstack`.
    - stack_adjust: Adjusts the base frame to reduce unnecessary frame queries.
        For instance, `stack_adjust = 0` means no adjustment is made, and the search starts from the next layer by default;
        `stack_adjust = 2` means the search starts from three layers down by default.
    - exc_info: Default is `True`, exception information is added to the logging message.
        If an exception tuple (in the format returned by sys.exc_info()) is provided, it is used.
        If it is None, which means no exception information is added.
    - stack_info: If True, stack information is added to the logging message.
    - stack_level: If provided, specifies which stack frame to use when logging the call.
        Default is 1, which means the immediate caller's frame.
    - extra: A dictionary of extra context to be added to the logging message.
        This can be used to pass additional information that can be used by the logging handlers.
        For example: extra={'user': 'Johnnny'}
    """
    target_level = get_stack_level(starts_with, stack_adjust + 1) if stack_level is None else stack_level + 1
    logging.exception(message, exc_info=exc_info, stack_info=stack_info, stacklevel=target_level, extra=extra)


def critical(
    message: str,
    starts_with: str = 'test',
    stack_adjust: int = 0,
    exc_info: bool | tuple | None = None,
    stack_info: bool = False,
    stack_level: int | None = None,
    extra: Mapping[str, object] | None = None
) -> None:
    """
    Calling logging.critical method, and finding stacklevel starts with specific function name.

    - message: The message format string, or an object to be logged.
        If it is an object, it is converted to a string using str().
    - starts_with: Records the log information in the function or module name that starts with the starts_with keyword.
        For example, `'test'` means the log will be displayed in the function `test_xxx()` or the module `test_xxx.py`.
        If both a module and a function have the same prefix, the function takes precedence.
        If the target is not found, it defaults to the first caller of this `logstack`.
    - stack_adjust: Adjusts the base frame to reduce unnecessary frame queries.
        For instance, `stack_adjust = 0` means no adjustment is made, and the search starts from the next layer by default;
        `stack_adjust = 2` means the search starts from three layers down by default.
    - exc_info: If True, exception information is added to the logging message.
        If an exception tuple (in the format returned by sys.exc_info()) is provided, it is used.
        Default is None, which means no exception information is added.
    - stack_info: If True, stack information is added to the logging message.
    - stack_level: If provided, specifies which stack frame to use when logging the call.
        Default is 1, which means the immediate caller's frame.
    - extra: A dictionary of extra context to be added to the logging message.
        This can be used to pass additional information that can be used by the logging handlers.
        For example: extra={'user': 'Johnnny'}
    """
    target_level = get_stack_level(starts_with, stack_adjust + 1) if stack_level is None else stack_level + 1
    logging.critical(message, exc_info=exc_info, stack_info=stack_info, stacklevel=target_level, extra=extra)


def get_stack_level(starts_with: str = 'test', stack_adjust: int = 0) -> int:
    """
    Finding the stacklevel which the funcname starts with `starts_with` string.

    Args:
    - starts_with: finding the target stack level which function name starts with it.
    - stack_adjust: setup the default stack level base on 1,
        e.g. stack_adjust = 2 -> default stack level will be 1 + 2 = 3
    """
    # Get the current frame.
    frame = inspect.currentframe()

    # stack = 0 represents the current frame, so +1 is to skip it.
    # If the user knows the specific number of frames to skip, they can set stack_adjust.
    stack = stack_default = stack_adjust + 1
    for _ in range(stack):
        frame = frame.f_back

    # Start searching through the subsequent frames.
    # Once a module or function matches the keyword, return it's stack.
    while frame:
        if frame.f_code.co_name.startswith(starts_with) or \
           os.path.basename(frame.f_code.co_filename).startswith(starts_with):
            return stack
        frame = frame.f_back
        stack += 1

    # If no matches are found, return the default stack.
    return stack_default


def get_stack_infos(
    starts_with: str = 'test',
    stack_adjust: int = 0,
    to_dict: bool = False
) -> str | dict[str, str]:
    """
    Finding the filename, lineno and funcname by funcname starts with `starts_with` string.

    Args:
    - starts_with: The string to search the function name which starts with.
    - stack_adjust: Adjust the start stack level.
    - to_dict: Determine the return type.

    Return:
    - to_dict is True: {'filename': 'xxx.py', 'lineno': '19', 'funcname': 'my_func'}
    - to_dict is False: '|xxx.py:19|my_func|'
    """
    # Get the current frame.
    frame = inspect.currentframe()

    # stack = 0 represents the current frame, so +1 is to skip it.
    # If the user knows the specific number of frames to skip, they can set stack_adjust.
    for _ in range(stack_adjust + 1):
        frame = frame.f_back

    # record the current starting frame and search for the one that matches the condition.
    # If no matching frame is found, use the default frame_target.
    frame_target = frame
    while frame:
        if frame.f_code.co_name.startswith(starts_with) or \
           os.path.basename(frame.f_code.co_filename).startswith(starts_with):
            frame_target = frame
            break
        frame = frame.f_back

    # After obtaining the final frame, return the filename, lineno, and funcname information.
    filename = os.path.basename(frame_target.f_code.co_filename)
    lineno = str(frame_target.f_lineno)
    funcname = frame_target.f_code.co_name

    # Let the user decide the format of the returned content.
    if to_dict:
        return {'filename': filename, 'lineno': lineno, 'funcname': funcname}
    return f'|{filename}:{lineno}|{funcname}|'


def _debug(message: str = '') -> None:
    if Log.RECORD:
        debug(message, stack_adjust=1)


def _info(message: str = '') -> None:
    if Log.RECORD:
        info(message, stack_adjust=1)


def _warning(message: str = '') -> None:
    if Log.RECORD:
        warning(message, stack_adjust=1)


def _error(message: str = '') -> None:
    if Log.RECORD:
        error(message, stack_adjust=1)


def _exception(message: str = '') -> None:
    if Log.RECORD:
        exception(message, stack_adjust=1)


def _critical(message: str = '') -> None:
    if Log.RECORD:
        critical(message, stack_adjust=1)
