import logging
import re

#
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
        # TODO: create my own exceptions, inhereted from class Exception
        raise Exception('Invoke `.with_logger()` to set your log')

    def with_logger(self, log=None):
        """Setter for the logger property, use None for default."""
        if not (log is None or isinstance(log, logging.Logger)):
            raise ValueError('`log` must be a Logger object or None')

        self._logger = log if log is not None else self._default_logger()

    def _default_logger(self):
        return logging.getLogger()

    @classmethod
    def before(cls, level, string):
        print('I make decorators! And I accept arguments:', string)
        attrs = cls._get_unique_params(string)
        print(attrs)
        print('\nprint ARGS:')
        for attr, prefix_str in attrs:
            if re.match('({\d+})', attr):
                cls._print_param(attr, prefix_str)

        def my_decorator(func):
            # The ability to pass arguments here is a gift from closures.
            # If you are not comfortable with closures, you can assume it's ok,
            # or read: http://stackoverflow.com/questions/13857/can-you-explain-closures-as-they-relate-to-python

            # print('I am the decorator. Somehow you passed me arguments:', string)

            # Don't confuse decorator arguments and function arguments!
            def wrapped_all(*args, **kwargs):
                #print('I am the wrapper around the decorated function.\n'
                #      'I can access all the variables\n'
                #      '\t- from the decorator: {0}\n'
                #      '\t- from the function call: {1} {2}\n'
                #      'Then I can pass them to the decorated function'
                #      .format(string, args, kwargs))
                #
                return func(args, kwargs)

            return wrapped_all

        return my_decorator

    @classmethod
    def _get_unique_params(cls, string):
        """
        Get a list of tuples with:
            1.  Special, well known, paramater.
            2.  String untill the parameter position.
        """
        #print(re.findall('({\d+})', 'first arg {0}second group {1}'))
        start_index = 0
        attr_tuples = []

        attrs = re.findall('({\d+})', string)
        for attr in attrs:
            curr_index = string.find(attr)
            attr_tuples.append((attr, string[start_index : curr_index]))
            start_index += curr_index + len(attr)

        return attr_tuples

    @classmethod
    def _print_param(cls, attr, prefix_str):
        print(prefix_str, attr) # instead of attr we will print(*args[in position])
