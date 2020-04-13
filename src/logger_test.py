import logging
import unittest

from logger import Logger


class TestLogger(unittest.TestCase):

    def test_before(self):
        # Arrange
        log = Logger('test/inputs', 'test/outputs')
        @log.before()
        def test(a, b=5, c='foo-bar', *args, **kwargs):
            pass
        @log.before()
        def test1(a, b=5, c='foo-bar', *args, **kwargs):
            pass

        # Act
        test('foo', 'bar')
        test1(1)
        test(1, 2)
        test(1, d='hello', output_names=['1'])
        test(1, 2, 3, 4, 5, f='hello', g='world')

    def test_after(self):
        # Arrange
        log = Logger('test/inputs', 'test/outputs')
        @log.after()
        def test(a, b=5, c='foo-bar', *args, **kwargs):
            return ['out_1'], 'out_2', 1
        @log.after()
        def test2(a, b=5, c='foo-bar', *args, **kwargs):
            return ['out_1'], 'out_2', 1

        # Act
        test('foo', 'bar')
        test2('foo', 'bar', output_names=['out1', 'out2', 'out3'])
        self.assertRaises(ValueError, test, 'foo', 'bar', output_names=['1'])
        self.assertRaises(ValueError, test, 'foo', 'bar', output_names=['1', '2', '3', '4'])

    def test_before_and_after(self):
        # Arrange
        log = Logger('test/inputs', 'test/outputs')
        @log.before_and_after()
        def test(a, b=5, c='foo-bar', *args, **kwargs):
            return ['out_1'], 'out_2', 1

        @log.before_and_after()
        def test3(a, b=5, c='foo-bar', *args, **kwargs):
            return ['out_1'], 'out_2', 1

        # Act
        test('foo', x='bar')
        test3(1, d='hello')
        test(1, 2, 3, 4, 5, f='hello', g='world')
        test('foo', 'bar', output_names=['out1', 'out2', 'out3'])
        self.assertRaises(ValueError, test, 'foo', 'bar', output_names=['1'])
        self.assertRaises(ValueError, test, 'foo', 'bar', output_names=['1', '2', '3', '4'])


if __name__ == '__main__':
    unittest.main()
