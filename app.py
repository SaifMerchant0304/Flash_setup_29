from flask import Flask, request, send_from_directory, redirect, url_for, render_template_string
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static'
PASSWORD = "Metro_CRM"  # Change this to your secret password

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML_FORM = """
<!doctype html>
<title>Upload VOC CSV</title>
<h2>CX-VOC Data Uploader</h2>
<form method=post enctype=multipart/form-data>
  <input type="password" name="password" placeholder="Enter Upload Password"><br><br>
  <input type="file" name="file"><br><br>
  <input type="submit" value="Upload">
</form>
<p>{{ message }}</p>
"""

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
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
