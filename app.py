from flask import Flask, render_template_string
import os
import urllib.request

app = Flask(__name__)

# Read environment variables
BACKGROUND_URL = os.environ.get('BACKGROUND_URL', '')
MYSQL_USER = os.environ.get('MYSQL_USER', 'default_user')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'default_password')
YOUR_NAME = os.environ.get('YOUR_NAME', 'Student')

# Download image from S3 to /tmp/background.jpg
def download_background():
    if BACKGROUND_URL:
        try:
            urllib.request.urlretrieve(BACKGROUND_URL, '/tmp/background.jpg')
            print(f"Background image downloaded from {BACKGROUND_URL}")
            return True
        except Exception as e:
            print(f"Error downloading image: {e}")
            return False
    return False

# Download background on startup
download_background()

# HTML template with CSS using local image path
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>My Web Application</title>
    <style>
        body {
            background-image: url('/tmp/background.jpg');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            font-family: Arial, sans-serif;
            color: white;
            text-align: center;
            padding: 50px;
            margin: 0;
            min-height: 100vh;
        }
        .container {
            background-color: rgba(0,0,0,0.7);
            padding: 30px;
            border-radius: 10px;
            display: inline-block;
        }
        h1 {
            color: #ff9900;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome, {{ name }}!</h1>
        <p><strong>MySQL User:</strong> {{ mysql_user }}</p>
        <p><strong>Application Status:</strong> Running successfully on port 81</p>
        <hr>
        <small>Containerized Web App - Phase 2</small>
    </div>
</body>
</html>
"""

@app.route('/')
def hello():
    return render_template_string(HTML_TEMPLATE, 
                                name=YOUR_NAME,
                                mysql_user=MYSQL_USER)

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
