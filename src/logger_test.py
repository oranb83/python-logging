import unittest
import logging

from logger import Logger

##
class TestLogger( unittest.TestCase ):

	#
	def test_logger_not_set( self ):
		""" A logger object was not set """

		# Assert
		self.assertRaises( Exception, lambda: Logger().logger )

	#
	def test_logger_set( self ):
		""" A logger object was set """

		# Arrange
		log = Logger()

		# Act
		log._logger = logging.Logger( "test" )

		# Assert
		self.assertIsNotNone( log.logger )

	#
	def test_with_logger_default( self ):
		""" Set a default logger """

		# Arrange
		log = Logger()
		expected = log._default_logger()

		# Act
		log.with_logger()

		# Assert
		self.assertEqual( expected, log.logger )

	#
	def test_with_logger_wrong_obj( self ):
		""" Set a None logger object """

		# Assert
		self.assertRaises( ValueError, Logger().with_logger, "test" )

	#
	def test_with_logger( self ):
		""" Set a logger object """

		# Arrange
		log = Logger()

		# Act
		log.with_logger( logging.getLogger() )

		# Assert
		self.assertIsNotNone( log.logger )


if __name__ == "__main__":
	unittest.main()
