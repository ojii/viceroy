(function(){
    var cache = {};

    QUnit.testStart(function(details){
        var name = details.name;
        VICEROY.start_test(name);
        cache[name] = [];
    });

    QUnit.log(function(details){
        if (!details.result){
            cache[details.name].push(details.message);
        }
    });

    QUnit.testDone(function(details){
        var messages;
        var name = details.name;
        if (details.failed !== 0){
            messages = ['Failed ' + details.failed + ' / ' + details.total + 'assertions:'];
            messages.push.apply(messages, cache[name]);
            VICEROY.fail(name, messages.join('\n'));
        } else {
            VICEROY.success(name);
        }
    });

    QUnit.done(function(){
        VICEROY.done();
    });
})();
