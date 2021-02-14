import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import datetime

UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = {}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = 10 * 1024 * 1024  # Max 10MB


@app.template_filter()
def datetimefilter(value, format='%Y/%m/%d %H:%M'):
    """convert a datetime to a different format."""
    return value.strftime(format)


app.jinja_env.filters['datetimefilter'] = datetimefilter


@app.route("/")
def home():
    return render_template('template.html', my_string="Wheeeee!",
                           my_list=[0,1,2,3,4,5], title="Index", current_time=datetime.datetime.now())


@app.route("/upload")
def upload():
    return render_template('upload.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('template_test'))

        return "File uploaded successfully"


if __name__ == '__main__':
    app.run(debug=True)
