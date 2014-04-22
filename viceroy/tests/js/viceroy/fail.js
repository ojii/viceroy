// test failure
VICEROY.start_test('test_fail');
VICEROY.fail('test_fail', 'expected_failure');
// test error
VICEROY.start_test('test_error');
throw "expected"
VICEROY.done()
