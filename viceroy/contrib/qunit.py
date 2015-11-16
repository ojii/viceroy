from viceroy.scanner import BaseScanner


class QUnitScanner(BaseScanner):
    test_methods = {
        'test': 0,
        'asyncTest': 0,
        'QUnit.test': 0,
        'QUnit.asyncTest': 0,
    }
