from typing import Callable, Any
from abc import ABC, abstractmethod
from functools import wraps


class Convertible(ABC):
    """
    A class to automatically convert an argument
    """

    @abstractmethod
    def convert(self, argument: Any) -> Any:
        """
        Converts the argument provided to a specified type.

        Parameters
        ----------
        argument : Any
            The argument to be converted.
        """


def ignore_self(decorator: Callable[[Callable], Any]):
    """
    A decorator to ignore the self variable passed for classes.
    This will automatically strip the variable if required.

    Parameters
    ----------
    decorator : Callable[[Callable], Any]
        The decorator that should ignore the self variable.
    """

    class FunctionMethodAdaptor:
        """
        A descriptor to peak to see if it is a method or function at runtime.
        """

        def __init__(self, decorator: Callable[[Callable], Any], func: Callable):
            self.decorator = decorator
            self.func = func

        def __get__(self, instance, owner):
            return self.decorator(self.func.__get__(instance, owner))

        def __call__(self, *args, **kwargs):
            return self.decorator(self.func)(*args, **kwargs)

    def ignore_self(func: Callable):
        return FunctionMethodAdaptor(decorator, func)

    return ignore_self


def convert(*args: Convertible, **kwargs: Convertible):
    """
    A decorator to automatically convert types with Convertibles.
    """

    convertable_args = args
    convertable_kwargs = kwargs

    @ignore_self
    def convert(func: Callable):
        """The middle wrapper for the decorator"""

        @wraps(func)
        def convert(*args, **kwargs):
            """
            For each argument provided, we will try to find a convertible.
            If none are found, then we will just pass the value provided.
            """

            new_args, new_kwargs = [], {}
            for idx, arg in enumerate(args):
                try:
                    new_args.append(convertable_args[idx].convert(arg))
                except IndexError:
                    new_args.append(arg)
            for idx, (key, value) in enumerate(kwargs.items()):
                try:
                    new_kwargs.update({key: convertable_kwargs[key].convert(value)})
                except KeyError:
                    new_kwargs.update({key: value})
            return func(*new_args, **new_kwargs)

        return convert

    return convert
