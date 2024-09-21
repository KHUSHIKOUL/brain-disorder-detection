from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename

# Create Flask app
app = Flask(__name__)
app.secret_key = 'some_secret_key'  # Change this for security

# Folder to save uploaded files
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'dcm'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        age = request.form['age']
        symptoms = request.form['symptoms']
        family_history = request.form['family_history']

        # Handle file upload
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')

            # Perform basic risk assessment (replace with actual ML model)
            disorder_risk = 'Low'
            if int(age) >= 60 or family_history != 'none' or 'memory loss' in symptoms:
                disorder_risk = 'High'
            elif 'headaches' in symptoms or 'confusion' in symptoms:
                disorder_risk = 'Moderate'

            return render_template('result.html', name=name, age=age, symptoms=symptoms,
                                   family_history=family_history, disorder_risk=disorder_risk)

    return render_template('index.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
  