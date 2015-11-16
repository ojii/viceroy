from viceroy.scanner import BaseScanner


def stop(node):
    raise StopIteration()


class JasmineScanner(BaseScanner):
    test_methods = {
        'it': 0,
        'xdescribe': stop
    }
