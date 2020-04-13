import os
import time
import inspect
import logging
from copy import deepcopy

FORMAT = ''
LOG_LEVEL = os.getenv('LOG_LEVEL', logging.getLevelName(logging.DEBUG))
DEFAUL_OUTPUT_NAME = 'output'

logging.basicConfig(format=FORMAT, level=LOG_LEVEL)


class Logger:
    """
    Advanced Logger using decorator to log ops before and after methods.
    """
    _logger_input = None
    _logger_output = None

    @property
    def logger_input(self):
        """
        Gets the logger property, if the .with_logger() method was
        invoked, otherwise raise an Exception.
        """
        if self._logger_input is not None:
            return self._logger_input

        # TODO: create my own custom exceptions, inhereted from class Exception
        raise Exception('Invoke logger.setter to set your log')

    @logger_input.setter
    def logger_input(self, log=None):
        """
        Setter for the logger property, use None for default.
        """
        if not (log is None or isinstance(log, logging.Logger)):
            raise ValueError('`log` must be a Logger object or None')

        self._logger_input = log if log is not None else self._default_logger('inputs')

    @property
    def logger_output(self):
        """
        Gets the logger property, if the .with_logger() method was
        invoked, otherwise raise an Exception.
        """
        if self._logger_output is not None:
            return self._logger_output

        # TODO: create my own custom exceptions, inhereted from class Exception
        raise Exception('Invoke logger.setter to set your log')

    @logger_output.setter
    def logger_output(self, log=None):
        """
        Setter for the logger property, use None for default.
        """
        if not (log is None or isinstance(log, logging.Logger)):
            raise ValueError('`log` must be a Logger object or None')

        self._logger_output = log if log is not None else self._default_logger('outputs')

    def _default_logger(self, filename):
        return logging.getLogger(f'{filename}_{time.strftime("%Y%m%d-%H%M%S")}.txt')

    def before(self, level):
        """
        Log all the method arguments.

        Use for methods that have arguments and you wish to log them.
        Usage:
            log = Logger()
            log.logger_input = None  # or a custom logger (this uses the default)
            @log.before(logging.INFO)
            def test(a, b=5, c='foo-bar', *args, **kwargs):
                pass

            test(['foo'], b=7, c={'k': 1})

        output will be:
            a : ['foo']
            b : 7
            c : {'k': 1}

        @note: all other positional arguments will be under args or kwargs keys
        @note: prints to stdout and filename (defaulted to inputs_<datetime>.txt)
        """
        def dump_args(func):
            """
            Decorator to print function call details - parameters names and effective values.
            """
            # The ability to pass arguments here is a gift from closures.
            # If you are not comfortable with closures, you can assume it's ok,
            # or read: http://stackoverflow.com/questions/13857/can-you-explain-closures-as-they-relate-to-python
            def wrapper(*args, **kwargs):
                kwargs.pop('output_names', None)
                func_args = inspect.signature(func).bind(*args, **kwargs).arguments
                func_args_str = '\n'.join('{} : {!r}'.format(*item) for item in func_args.items())
                self.logger_input.log(level, func_args_str)
                return func(*args, **kwargs)

            return wrapper

        return dump_args

    def after(self, level):
        """
        Log all the method output.

        Use for methods that have outputs and you wish to log them.
        Usage:
            log = Logger()
            log.logger_output = None  # or a custom logger (this uses the default)
            @log.before(logging.INFO)
            def test(a, b=5, c='foo-bar', output_names=['o1, o2, o3'], *args, **kwargs):
                return 1, ['foo', 'bar'], 'hello'

            test(['foo'], b=7, c={'k': 1})

        output will be:
            o1 : 1
            o2 : ['foo', 'bar']
            o3 : 'hello'

        @note: if output_names is missing or None, the output keys will be:
               <DEFAUL_OUTPUT_NAME>_<index>
        @note: prints to stdout and filename (defaulted to outputs_<datetime>.txt)
        @raise: ValueError in case of wrong amount of output_names supplied.
        """
        def dump_args(func):
            """
            Decorator to print function call details - output names and effective values.
            """
            # The ability to pass arguments here is a gift from closures.
            # If you are not comfortable with closures, you can assume it's ok,
            # or read: http://stackoverflow.com/questions/13857/can-you-explain-closures-as-they-relate-to-python
            def wrapper(*args, **kwargs):
                func_args = inspect.signature(func).bind(*args, **kwargs).arguments
                func_output_keys = func_args.get('kwargs', {}).get('output_names')
                func_output_values = func(*args, **kwargs)
                if not isinstance(func_output_values, tuple):
                    func_output_values = (func_output_values,)
                if func_output_keys is None:
                    func_output_keys = [
                        f'{DEFAUL_OUTPUT_NAME}_{i}' for i in range(1, len(func_output_values) + 1)]
                elif len(func_output_keys) != len(func_output_values):
                    raise ValueError(f'Expected {len(func_output_keys)} output_names, '
                                     f'but {len(func_output_values)} output_names were provided')
                func_args_str = '\n'.join('{} : {!r}'.format(*item) for item in zip(
                    func_output_keys, func_output_values))
                self.logger_output.log(level, func_args_str)
                return func(*args, **kwargs)

            return wrapper

        return dump_args

    def before_and_after(self, level):
        """
        Log all the method arguments and output.

        Use for methods that have outputs and you wish to log them.
        Usage:
            log = Logger()
            log.logger_output = None  # or a custom logger (this uses the default)
            @log.before(logging.INFO)
            def test(a, b=5, c='foo-bar', output_names=['o1, o2, o3'], *args, **kwargs):
                return 1, ['foo', 'bar'], 'hello'

            test(['foo'], b=7, c={'k': 1})

        output will be:
            a : ['foo']
            b : 7
            c : {'k': 1}
            o1 : 1
            o2 : ['foo', 'bar']
            o3 : 'hello'

        @note: all other positional arguments will be under args or kwargs keys
        @note: if output_names is missing or None, the output keys will be:
               <DEFAUL_OUTPUT_NAME>_<index>
        @note: prints to stdout and filename (defaulted to outputs_<datetime>.txt)
        @raise: ValueError in case of wrong amount of output_names supplied.
        """
        def dump_args(func):
            """
            Decorator to print function call details - input names and
            output names and effective values.
            """
            # The ability to pass arguments here is a gift from closures.
            # If you are not comfortable with closures, you can assume it's ok,
            # or read: http://stackoverflow.com/questions/13857/can-you-explain-closures-as-they-relate-to-python
            def wrapper(*args, **kwargs):
                # print arguments
                func_output_keys = kwargs.pop('output_names', None)
                func_args = inspect.signature(func).bind(*args, **kwargs).arguments
                func_args_str = '\n'.join('{} : {!r}'.format(*item) for item in func_args.items())
                self.logger_input.log(level, func_args_str)

                # print output
                func_output_values = func(*args, **kwargs)
                if not isinstance(func_output_values, tuple):
                    func_output_values = (func_output_values,)
                if func_output_keys is None:
                    func_output_keys = [
                        f'{DEFAUL_OUTPUT_NAME}_{i}' for i in range(1, len(func_output_values) + 1)]
                elif len(func_output_keys) != len(func_output_values):
                    raise ValueError(f'Expected {len(func_output_keys)} output_names, '
                                     f'but {len(func_output_values)} output_names were provided')
                func_args_str = '\n'.join('{} : {!r}'.format(*item) for item in zip(
                    func_output_keys, func_output_values))
                self.logger_output.log(level, func_args_str)
                return func(*args, **kwargs)

            return wrapper

        return dump_args
