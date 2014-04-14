(function(){
    QUnit.log(function(details){
        viceroy_notify(!details.result, details.message);
    });
})();
