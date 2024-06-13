from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import subprocess
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads/'
PROCESSED_FOLDER = 'processed/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            csv_path = os.path.join(PROCESSED_FOLDER, file.filename.rsplit('.', 1)[0] + '.csv')
            # Convert TXT to CSV
            subprocess.run(['python', 'converter.py', filepath, csv_path])
            # Execute Jupyter notebook for graph
            subprocess.run(['jupyter', 'nbconvert', '--to', 'notebook', '--execute', 'MODEL.ipynb', '--output', 'MODEL_out.ipynb'])
            # Execute another Jupyter notebook for text generation
            subprocess.run(['jupyter', 'nbconvert', '--to', 'notebook', '--execute', 'ANOTHER_MODEL.ipynb', '--output', 'ANOTHER_MODEL_out.ipynb'])
            return redirect(url_for('results', filename='result_page.html'))
    return render_template('index.html')

@app.route('/results/<filename>')
def results(filename):
    return send_from_directory(PROCESSED_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
