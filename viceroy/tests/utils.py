from viceroy.scanner import BaseScanner


class ViceroyScanner(BaseScanner):
    test_methods = {
        'VICEROY.store_result': 0,
        'VICEROY.success': 0,
        'VICEROY.fail': 0,
        'VICEROY.skip': 0,
        'VICEROY.start_test': 0,
    }
