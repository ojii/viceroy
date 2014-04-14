function viceroy_send(data){
    console.log('viceroy_send');
    var url = window.location.protocol + '//' + window.location.host + '/viceroy-api/';
    console.log(url);
    var request = new XMLHttpRequest();
    request.onreadystatechange = function(event){
        console.log(request);
        console.log(request.readyState);
        console.log(event);
    };
    request.open('POST', url);
    request.setRequestHeader('Content-Type', 'application/json');
    request.send(JSON.stringify(data));
}

function viceroy_notify(failed, error_msg){
    console.log('viceroy_notify');
    viceroy_send({'failed': failed, 'message': error_msg});
}

window.onerror = function(msg, url, lineno){
    viceroy_send({'failed': true, 'message': 'Error: ' + url + ':' + lineno + '\n' + msg});
}
