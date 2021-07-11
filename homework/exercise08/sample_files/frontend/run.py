import os

import pandas as pd

from plab2.utils import Profiler
from plab2.startup import DATA_DIR
from plab2.network import Analyzer
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, url_for, render_template


UPLOAD_FOLDER = os.path.join(DATA_DIR, 'uploads')
ALLOWED_EXTENSIONS = {"tsv", "csv"}

app = Flask(__name__)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = 16 * 1024 * 1024


@app.route("/")
def home():
    return render_template('template.html', my_list=[0, 1, 2, 3, 4])


@app.route("/upload")
def upload():
    return render_template('upload.html')


@app.route("/paths", methods=['POST'])
def find_shortest_paths():
    values = [x.strip() for x in request.form['textbox'].split(",")]
    if len(values) != 2:
        error_msg_html = "More than 2 HGNC symbols were passed!"
        return render_template('template.html', paths_header=error_msg_html)

    source, target = values
    uploaded_files = os.listdir(UPLOAD_FOLDER)

    if uploaded_files == 0:
        error_msg_html = "No PPI File Found!"
        return render_template('template.html', paths_header=error_msg_html)

    ppi = os.path.join(UPLOAD_FOLDER, uploaded_files[0])
    path_finder = Analyzer(ppi_file=ppi)
    sp = path_finder.shortest_paths(source.upper(), target.upper())

    if not sp:
        error_msg_html = f"No paths found for <b>{source.upper()} and {target.upper()}</b>"
        return render_template('template.html', paths_header=error_msg_html)

    else:
        sp_names = [path_finder.nodes[node_id]['symbol'] for node_id in sp[0]]
        pos_html = f"Shortest path for {source.upper()} and {target.upper()}"
        return render_template('template.html', paths_header=pos_html, shortest_path=sp_names)


@app.route("/get_info", methods=['POST'])
def get_hgnc_info():
    """Retrieves identifier information for a given HGNC symbol."""
    report_url_tmp = "https://www.genenames.org/data/gene-symbol-report/#!/hgnc_id/{}"
    symbol = request.form['textbox']
    ids = Profiler(symbol.upper()).get_identifers()
    if ids:
        ids['uniprot'] = ids['uniprot'][:1]  # Only take first UniProt ID
        id_table = pd.DataFrame(ids)
        id_table_html = f"<h4>Results for: <b>{symbol.upper()}</b></h4>" + \
                        id_table.to_html(header="true", table_id="table", index=False)

        # hgnc_id = ids['hgnc']
        # "For more information, visit {report_url_tmp.format(hgnc_id)}"

    else:
        id_table_html = f"No information found for {symbol}"

    return render_template('template.html', symbol_name=symbol.upper(), hgnc_info=id_table_html)


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
            return render_template('template.html', success_msg="File uploaded successfully")

        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
