(function(){
    var ViceroyReporter = function(){
        this.specStarted = function(result){
            VICEROY.start_test(result.description);
        };

        this.specDone = function(result){
            if (result.failedExpectations !== 0){
                var messages = ['Failed expectations: ' + result.failedExpectations];
                for (var index = 0; index < result.failedExpectations.length; index++){
                    messages.push(result.failedExpectations[index].message);
                }
                VICEROY.fail(messages.join('\n'));
            } else {
                VICEROY.success(result.description);
            }
        };

        this.jasmineDone = function(){
            VICEROY.done();
        };
    };
    jasmine.getEnv().addReporter(new ViceroyReporter());
})();
