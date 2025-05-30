from flask import Flask, request, send_from_directory, render_template_string
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

UPLOAD_FOLDER = 'static'
PASSWORD = "Metro_CRM"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML_FORM = """<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Upload VOC CSV</title>
    <style>
        body {
            background-color: #ffffff;
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            padding: 0;
        }
        h2 {
            color: #d32f2f;
            margin-bottom: 20px;
        }
        form {
            background-color: #fff0f0;
            border: 2px solid #d32f2f;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0px 0px 10px rgba(211, 47, 47, 0.2);
            width: 300px;
            text-align: center;
        }
        input[type="password"],
        input[type="file"] {
            width: 100%;
            padding: 8px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        input[type="submit"] {
            background-color: #d32f2f;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 5px;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background-color: #b71c1c;
        }
        p {
            margin-top: 15px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h2>CX-VOC Data Uploader</h2>
    <form method="post" enctype="multipart/form-data">
        <input type="password" name="password" placeholder="Enter Upload Password" required><br>
        <input type="file" name="file" required><br>
        <input type="submit" value="Upload CSV">
    </form>
    <p>{{ message }}</p>
</body>
</html>"""

@app.route('/', methods=['GET', 'POST'])
def upload():
    message = ''
    if request.method == 'POST':
        if request.form.get('password') != PASSWORD:
            message = '❌ Unauthorized access.'
        else:
            f = request.files['file']
            f.save(os.path.join(UPLOAD_FOLDER, 'latest_data.csv'))
            message = '✅ Upload successful. File saved as latest_data.csv'
    return render_template_string(HTML_FORM, message=message)

@app.route('/latest_data.csv')
def serve_csv():
    return send_from_directory(UPLOAD_FOLDER, 'latest_data.csv')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)