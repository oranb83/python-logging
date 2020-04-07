import os
import inspect
import logging
from functools import wraps

FORMAT = ''
LOG_LEVEL = os.getenv('LOG_LEVEL', logging.getLevelName(logging.DEBUG))

logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=FORMAT)


class Logger:
    """
    Advanced Logger using decorator to log ops before and after methods
    """
    _logger = None

    @property
    def logger(self):
        """
        Gets the logger property, if the .with_logger() method was invoked,
        Otherwise raise an Exception.
        """
        if self._logger is not None:
            return self._logger

        # TODO: create my own custom exceptions, inhereted from class Exception
        raise Exception('Invoke logger.setter to set your log')

    @logger.setter
    def logger(self, log=None):
        """Setter for the logger property, use None for default."""
        if not (log is None or isinstance(log, logging.Logger)):
            raise ValueError('`log` must be a Logger object or None')

        self._logger = log if log is not None else self._default_logger()

    def _default_logger(self):
        return logging.getLogger()

    def before(self, level):
        """
        Log all the method arguments.
        """
        def dump_args(func):
            """
            Decorator to print function call details - parameters names and effective values.
            """
            # The ability to pass arguments here is a gift from closures.
            # If you are not comfortable with closures, you can assume it's ok,
            # or read: http://stackoverflow.com/questions/13857/can-you-explain-closures-as-they-relate-to-python
            def wrapper(*args, **kwargs):
                func_args = inspect.signature(func).bind(*args, **kwargs).arguments
                func_args_str = '\n'.join('{} : {!r}'.format(*item) for item in func_args.items())
                self.logger.log(level, func_args_str)
                return func(*args, **kwargs)

            return wrapper

        return dump_args
