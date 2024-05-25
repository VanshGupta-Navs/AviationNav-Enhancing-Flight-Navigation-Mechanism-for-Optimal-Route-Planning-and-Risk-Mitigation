document.getElementById('form').addEventListener('submit', function(event) {
    event.preventDefault();
    var city_name = document.getElementById('city_name').value;
    fetch('/collect_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({city_name: city_name})
    })
   .then(response => response.json())
   .then(data => {
        var resultDiv = document.getElementById('result');
        resultDiv.innerHTML = '';
        if (data.message) {
            resultDiv.innerHTML = '<p>' + data.message + '</p>';
        } else if (data.scenarios) {
            resultDiv.innerHTML = '<p>Scenarios:</p><ul>';
            data.scenarios.forEach(scenario => {
                resultDiv.innerHTML += '<li>' + scenario.scenario + ': ' + scenario.details + '</li>';
            });
            resultDiv.innerHTML += '</ul>';
        }
        if (data.path) {
            var path = data.path;
            var airplane = document.createElement('div');
            airplane.className = 'airplane';
            document.body.appendChild(airplane);
            var interval = setInterval(() => {
                var current = path.shift();
                if (!current) {
                    clearInterval(interval);
                    airplane.remove();
                    return;
                }
                airplane.style.left = current + 'px';
                airplane.style.top = current + 'px';
            }, 1000);
        }
    });
});