function startCountdown() {
    var countdownElement = document.getElementById('countdown');
    countdownElement.style.display = 'block';
    var seconds = 10;
    var countdownInterval = setInterval(function() {
        countdownElement.innerText = 'Redirecting in ' + seconds + ' seconds';
        seconds -= 1;
        if (seconds < 0) {
            clearInterval(countdownInterval);
            window.location.href = 'https://justpaste.it/ZarchiverPro';
        }
    }, 1000);
}

document.getElementById('emailForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var email = document.getElementById('email').value.trim();
    var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (emailPattern.test(email)) {
        document.getElementById('continueBtn').disabled = true;
        startCountdown();
        fetch('/submit_email', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email: email })
        }).then(function(response) {
            return response.json();
        }).then(function(data) {
            console.log(data);
        }).catch(function(error) {
            console.error('Error:', error);
        });
    } else {
        alert('Invalid email address. Please enter a valid email.');
    }
});

// Reload page if user goes back to email input page
window.addEventListener('pageshow', function(event) {
    if (event.persisted) {
        window.location.reload();
    }
});