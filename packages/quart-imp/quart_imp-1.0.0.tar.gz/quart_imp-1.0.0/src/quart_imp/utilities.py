import functools
import logging
import re
import sys
import typing as t
from pathlib import Path


class Sprinkles:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def deprecated(message: str) -> t.Callable[[t.Any], t.Any]:
    def func_wrapper(func: t.Any) -> t.Any:
        @functools.wraps(func)
        def proc_function(*args: t.Any, **kwargs: t.Any) -> t.Any:
            logging.warning(
                f"{Sprinkles.FAIL}Function deprecated: {message}{Sprinkles.END}"
            )
            return func(*args, **kwargs)

        return proc_function

    return func_wrapper


def cast_to_import_str(app_name: str, folder_path: Path) -> str:
    """
    Takes the folder path and converts it to a string that can be imported
    """
    folder_parts = folder_path.parts
    parts = folder_parts[folder_parts.index(app_name) :]
    if sys.version_info.major == 3:
        if sys.version_info.minor < 9:
            return ".".join(parts).replace(".py", "")
        return ".".join(parts).removesuffix(".py")
    raise NotImplementedError("Python version not supported")


def snake(value: str) -> str:
    """
    Switches name of the class CamelCase to snake_case
    """
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", value)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def slug(value: str) -> str:
    """
    Switches name of the class CamelCase to slug-case
    """
    value = value.replace("_", "-")
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1-\2", value)
    return re.sub("([a-z0-9])([A-Z])", r"\1-\2", s1).lower()


def class_field(class_: str, field: str) -> str:
    """
    Switches name of the class CamelCase to snake_case and tacks on the field name

    Used for SQLAlchemy foreign key assignments

    INFO ::: This function may not produce the correct information if you are using __tablename__ in your class
    """
    return f"{snake(class_)}.{field}"
