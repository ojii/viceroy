// test success
VICEROY.start_test('test_success');
VICEROY.success('test_success');
// test skip
VICEROY.start_test('test_skip');
VICEROY.skip('test_skip', 'testing skip');
// test expected failure
VICEROY.start_test('test_expected_failure');
VICEROY.expected_failure('test_expected_failure');
VICEROY.done();
