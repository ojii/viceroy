(function(){
    var results = [];
    QUnit.log(function(details){
        console.log('QUnit.log: ' + details);
        results.push(details);
    });
    QUnit.done(function(){
        Viceroy.done(results);
    });
})();
