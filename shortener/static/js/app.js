document.addEventListener('DOMContentLoaded', function() {
    var submitBtn = document.getElementById('form-submit');
    var linkInput = document.getElementById('link-input');
    var identifierInput = document.getElementById('identifier-input');
    var extensionInput = document.getElementById('extension-input');
    var CSRF_TOKEN = document.querySelector('input[type=hidden]').value

    linkInput.addEventListener('focus', function() {
        this.select();
        submitBtn.className = '';
        identifierInput.value = '';
        extensionInput.value = '';
    })
    
    identifierInput.addEventListener('focus', function() {
        identifierInput.placeholder = 'name';
        identifierInput.className = '';
    })

    submitBtn.addEventListener('click', function(e) {
        e.preventDefault();

        submitBtn.className = "loading";

        request('/add/', {
            link: linkInput.value,
            identifier: identifierInput.value,
            extension: extensionInput.value
        }, function(res) {
            switch(res.msg) {
                case 'succesfully_created':
                    submitBtn.className = 'success';
                    linkInput.value = 'http://' + window.location.hostname + '/' + res.data
                    break;
                case 'identifier_exists':
                    identifierInput.value = '';
                    identifierInput.placeholder = 'Used';
                    identifierInput.className = "error"
                    break;
            }
        })
    })

    function request(url, data, callback) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', url, true);
        xhr.setRequestHeader("X-CSRFToken", CSRF_TOKEN);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');

        xhr.send(queryStringify(data));
            
        xhr.onreadystatechange = function() {
            var DONE = 4; 
            var OK = 200;
            
            if (xhr.readyState === DONE) {
                if (xhr.status === OK) {
                    try {
                        var body = JSON.parse(xhr.responseText)
                    } catch(e) {
                        console.log(e);
                        return;
                    }
                    
                    callback(body);
                } else {
                    console.log('Error: ' + xhr.status);
                }
            }
        }
    }
    
    function queryStringify(data) {
       var ret = [];
       for (var d in data)
          ret.push(encodeURIComponent(d) + "=" + encodeURIComponent(data[d]));
       ret = ret.join("&");
       return ret.substr(0, ret.length - 1)
    }
});