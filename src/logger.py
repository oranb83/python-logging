import logging

#
class Logger( object ):
    """ 
    Advanced Logger using decorator to log ops before and after methods 
    """

    #
    def __init__( self ):
        self._logger = None

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
