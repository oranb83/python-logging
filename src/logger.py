import logging

#
class Logger( object ):
    """ 
    Advanced Logger using decorator to log ops before and after methods 
    """

    _logger = None

    @property
    def logger( self ):
        """ 
        Gets the logger property, if the .with_logger() method was invoked,
        Otherwise raise an Exception.
        """
        if self._logger is not None:
            return self._logger
        # TODO: create my own exceptions, inhereted from class Exception
        raise Exception( "Invoke `.with_logger()` to set your log" )

    #
    def with_logger( self, log = None ):
        """ Setter for the logger property, use None for default """
        if not ( log is None or isinstance( log, logging.Logger ) ):
            raise ValueError( "`log` must be a Logger object or None" )

        self._logger = log if log is not None else self._default_logger()

    #
    def _default_logger( self ):
        return logging.getLogger()

    #
    @classmethod
    def before( self, level, decorator_arg1, decorator_arg2 ):

        print "I make decorators! And I accept arguments:", decorator_arg1, decorator_arg2

        def my_decorator( func ):
            # The ability to pass arguments here is a gift from closures.
            # If you are not comfortable with closures, you can assume it's ok,
            # or read: http://stackoverflow.com/questions/13857/can-you-explain-closures-as-they-relate-to-python
            print "I am the decorator. Somehow you passed me arguments:", decorator_arg1, decorator_arg2

            # Don't confuse decorator arguments and function arguments!
            def wrapped( function_arg1, function_arg2 ) :
                print ( "I am the wrapper around the decorated function.\n"
                      "I can access all the variables\n"
                      "\t- from the decorator: {0} {1}\n"
                      "\t- from the function call: {2} {3}\n"
                      "Then I can pass them to the decorated function"
                      .format( decorator_arg1, decorator_arg2,
                              function_arg1, function_arg2 ) )
                return func( function_arg1, function_arg2 )

            return wrapped

        return my_decorator