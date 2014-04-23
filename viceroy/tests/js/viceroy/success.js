// test success
VICEROY.start_test('test_success');
VICEROY.success('test_success');
// test skip
VICEROY.start_test('test_skip');
VICEROY.skip('test_skip', 'testing skip');
VICEROY.done();
