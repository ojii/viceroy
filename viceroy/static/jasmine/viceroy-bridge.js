(function(){
    var ViceroyReporter = function(){
        this.results = [];
    };
    ViceroyReporter.prototype = new jasmine.JsApiReporter({});
    ViceroyReporter.prototype.specDone = function(result) {
        if (result.failedExpectations.length != 0){
            viceroy_notify(true, result.failedExpectations[i].message);
        } else {
            viceroy_notify(false, '');
        }
    };

    jasmine.getEnv().addReporter(new ViceroyReporter());
})();
