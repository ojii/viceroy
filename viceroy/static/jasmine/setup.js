(function(){
    var ViceroyReporter = function(){
        this.results = [];
    };
    ViceroyReporter.prototype = new jasmine.JsApiReporter({});
    ViceroyReporter.prototype.jasmineDone = function(){
        Viceroy.done(this.results);
    };

    ViceroyReporter.prototype.specDone = function(result) {
        var tmp;
        if (result.failedExpectations.length != 0){
            for (var i = 0, l = result.failedExpectations.length; i < l; i++){
                tmp = result.failedExpectations[i];
                this.results.push({
                    'passed': false,
                    'name': result.description,
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

    jasmine.getEnv().addReporter(new ViceroyReporter());
    window.onload(); // needed by boot.js
})();
