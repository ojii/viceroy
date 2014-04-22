VICEROY = {
    'SUCCESS': '.',
    'FAILURE': 'F',
    'EXCEPTION': 'E',
    'SKIP': 's',
    'EXPECTED_FAILURE': 'x',
    'RESULTS': {},
    'DONE': false,
    '_test_name': null,
    'success': function(test_name){
        VICEROY.store_result(test_name, VICEROY.SUCCESS, '');
    },
    'fail': function(test_name, reason){
        VICEROY.store_result(test_name, VICEROY.FAILURE, reason);
    },
    'expected_failure': function(test_name){
        VICEROY.store_result(test_name, VICEROY.EXPECTED_FAILURE, '');
    },
    'skip': function(test_name, reason){
        VICEROY.store_result(test_name, VICEROY.SKIP, reason);
    },
    'store_result': function(test_name, code, message){
        VICEROY.RESULTS[test_name] = {
            'code': code,
            'message': message
        }
        VICEROY._test_name = null;
    },
    'done': function(){
        VICEROY.DONE = true;
    },
    'start_test': function(test_name){
        VICEROY._test_name = test_name;
    },
    '_handle_error': function(msg, url, lineno){
        VICEROY.store_result(
            VICEROY._test_name || 'viceroy_javascript_error',
            VICEROY.EXCEPTION,
            'Error in ' + url + ':' + lineno + ':' + '\n' + msg
        );
        VICEROY.done();
    }
};

window.onerror = function(msg, url, lineno){
    VICEROY._handle_error(msg, url, lineno);
};
