window.viceroy_start = function(){
    var PJTVSReporter = function(){
        this.results = [];
    };
    PJTVSReporter.prototype = new jasmine.JsApiReporter({});
    PJTVSReporter.prototype.jasmineDone = function(){
        window.viceroy_done(this.results);
    };

    PJTVSReporter.prototype.specDone = function(result) {
        var tmp;
        if (result.failedExpectations.length != 0){
            for (var i = 0, l = result.failedExpectations.length; i < l; i++){
                tmp = result.failedExpectations[i];
                this.results.push({
                    'passed': false,
                    'name': result.description + ' (' + (i + 1) + ')',
                    'message': tmp.message,
                    'actual': tmp.actual,
                    'expected': tmp.expected
                });
            }
        } else {
            this.results.push({
                'passed': true,
                'name': result.description,
                'message': '',
                'actual': null,
                'expected': null
            });
        }
    };

    jasmine.getEnv().addReporter(new PJTVSReporter());

    var script = document.createElement('script');
    script.src = '/tests.js';
    script.onload = function(){
        jasmine.getEnv().execute();
    };
    document.documentElement.appendChild(script);
};
