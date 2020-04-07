import logging
import unittest

from logger import Logger


class TestLogger(unittest.TestCase):

	def test_logger_not_set(self):
		"""A logger object was not set"""
		# Assert
		self.assertRaises(Exception, lambda: Logger().logger)

	def test_logger_set(self):
		"""A logger object was set"""
		# Arrange
		log = Logger()

		# Act
		log.logger = logging.Logger('test')

		# Assert
		self.assertIsNotNone(log.logger)

	def test_with_logger_default(self):
		"""Set a default logger"""
		# Arrange
		log = Logger()
		expected = log._default_logger()

		# Act
		log.logger = None

		# Assert
		self.assertEqual(expected, log.logger)

	def test_with_logger(self):
		"""Set a logger object"""
		# Arrange
		log = Logger()

		# Act
		log.logger = logging.getLogger()

		# Assert
		self.assertIsNotNone(log.logger)

	def test_before(self):
		# Arrange
		log = Logger()
		log.logger = None
		@log.before(logging.INFO)
		def test(a, b=5, c='foo-bar', *args, **kwargs):
		    pass

		# Act
		test('Rajesh', 'Howard')
		test(1)
		test(1, 2)
		test(1, d='hello')
		test(1, 2, 3, 4, 5, f='hello', g='world')


if __name__ == '__main__':
	unittest.main()
