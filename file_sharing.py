from flask import Flask, send_from_directory, request, render_template_string
import socket
import os

app = Flask(__name__)

# Directory where your file is stored
SHARE_FOLDER = os.path.abspath("shared_files")

if not os.path.exists(SHARE_FOLDER):
    os.makedirs(SHARE_FOLDER)

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>File Sharing</title>
</head>
<body>
    <h2>Available Files for Download</h2>
    <ul>
    {% for file in files %}
        <li><a href="/download/{{ file }}">{{ file }}</a></li>
    {% endfor %}
    </ul>
</body>
</html>
"""

@app.route("/")
def index():
    files = os.listdir(SHARE_FOLDER)
    return render_template_string(HTML_TEMPLATE, files=files)

@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(SHARE_FOLDER, filename, as_attachment=True)

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))  # just to detect local IP (no internet needed)
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

if __name__ == "__main__":
    host_ip = get_local_ip()
    print(f"\n📂 Place files inside the folder: {SHARE_FOLDER}")
    print(f"🚀 Open this on other devices: http://{host_ip}:5000\n")
    app.run(host="0.0.0.0", port=5000, debug=False)
