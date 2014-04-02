window.Viceroy = new (function(){
    var _done = false;
    var _results = [];

    this.done = function(results){
        _results = results;
        _done = true;
    };

    this.results = function(){
        return _results;
    };

    this.is_done = function(){
        return _done;
    };

    this.get_results = function(){
        return _results;
    }
})();
