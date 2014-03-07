window.pjtvs_start = function(){
    var results = [];
    QUnit.config.autostart = false;
    QUnit.log(function(details){
        results.push(details);
    });
    QUnit.done(function(){
        window.pjtvs_done(results);
    })
    var script = document.createElement('script');
    script.src = '/tests.js';
    script.onload = function () {
        QUnit.init();
    };
    document.documentElement.appendChild(script);
};
