from collections import namedtuple
import unittest


Result = namedtuple('Result', 'name passed message')
ComparisonResult = namedtuple('Result', 'name passed message expected actual')


def test_method_factory(result):
    def test_method(self):
        if not result.passed:
            if isinstance(result, ComparisonResult):
                self.assertEqual(
                    result.actual,
                    result.expected,
                    result.message
                )
            else:
                self.fail(result.message)
    test_method.__doc__ = result.name
    return test_method


def build_test_cases(name, results):
    attrs = {}
    for i, result in enumerate(results):
        attrs['test_method'.format(i)] = test_method_factory(result)
        yield type(name, (unittest.TestCase,), attrs)('test_method')


def timeout_factory(exc):
    def test_timed_out(self):
        raise exc
    return test_timed_out


def build_timeout_test_case(name, exc):
    attrs = {'test_method': timeout_factory(exc)}
    yield type(name, (unittest.TestCase, ), attrs)('test_method')
