import os
import inspect
import logging

DEFAUL_OUTPUT_NAME = 'output'

logging.basicConfig(format='', level=logging.DEBUG)


class Logger:
    """
    Advanced Logger using decorator to log ops before and after methods.
    """
    def __init__(self, input_dir, output_dir=None):
        self.input_dir = input_dir
        # If the output_dir is not passes, we will use the same directory for both input and ouput
        self.output_dir = output_dir if output_dir is not None else input_dir
        # Generate input and output directories if they are missing
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

    def before(self):
        """
        Log all the method arguments.

        Use for methods that have arguments and you wish to log them.
        Usage:
            log = Logger('inputs', 'outputs') -> directories to save the logs
            @log.before()
            def test(a, b=5, c='foo-bar', *args, **kwargs):
                pass

            test(['foo'], b=7, c={'k': 1})

        output will be:
            a : ['foo']
            b : 7
            c : {'k': 1}

        @note: all other positional arguments will be under args or kwargs keys
        @note: prints to stdout and filename (defaulted to <input_dir>/<func_name>_inputs.txt)
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
                logger = logging.getLogger('before')
                logger.addHandler(
                    logging.FileHandler(filename=f'{self.input_dir}/{func.__name__}_inputs.txt'))
                logger.info(func_args_str)
                return func(*args, **kwargs)

            return wrapper

        return dump_args

    def after(self):
        """
        Log all the method output.

        Use for methods that have outputs and you wish to log them.
        Usage:
            log = Logger('inputs', 'outputs') -> directories to save the logs
            @log.after()
            def test(a, b=5, c='foo-bar', output_names=['o1, o2, o3'], *args, **kwargs):
                return 1, ['foo', 'bar'], 'hello'

            test(['foo'], b=7, c={'k': 1})

        output will be:
            o1 : 1
            o2 : ['foo', 'bar']
            o3 : 'hello'

        @note: if output_names is missing or None, the output keys will be:
               <DEFAUL_OUTPUT_NAME>_<index>
        @note: prints to stdout and filename (defaulted to <output_dir>/<func_name>_outputs.txt)
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
                logger = logging.getLogger('after')
                logger.addHandler(
                    logging.FileHandler(filename=f'{self.output_dir}/{func.__name__}_outputs.txt'))
                logger.info(func_args_str)
                return func(*args, **kwargs)

            return wrapper

        return dump_args

    def before_and_after(self):
        """
        Log all the method arguments and output.

        Use for methods that have both inputs and outputs and you wish to log them.
        Usage:
            log = Logger('inputs', 'outputs') -> directories to save the logs
            @log.before_and_after()
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
        @note: prints to stdout and filename (defaulted to:
            1. <input_dir>/<func_name>_inputs.txt
            2. <output_dir>/<func_name>_outputs.txt
        )
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
                logger = logging.getLogger('before')
                logger.addHandler(
                    logging.FileHandler(filename=f'{self.input_dir}/{func.__name__}_inputs.txt'))
                logger.info(func_args_str)

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
                logger = logging.getLogger('after')
                logger.addHandler(
                    logging.FileHandler(filename=f'{self.output_dir}/{func.__name__}_outputs.txt'))
                logger.info(func_args_str)
                return func(*args, **kwargs)

            return wrapper

        return dump_args
