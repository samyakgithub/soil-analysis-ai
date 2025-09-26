from flask import Flask, render_template, request, redirect, url_for
import os
from soil_utils import parse_soil_report, recommend_fertilizer, recommend_crop

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Upload file
        file = request.files.get('file')
        crop = request.form.get('crop')
        if not file or file.filename == '':
            return "No file selected", 400
        if not crop:
            return "Please enter crop name", 400

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Parse soil report from PDF
        soil_data = parse_soil_report(filepath)

        # Check crop suitability
        suitability = recommend_crop(soil_data, crop)

        # Get fertilizer recommendation (based on soil and crop)
        fertilizer = recommend_fertilizer(soil_data, crop)

        return render_template('index.html', soil=soil_data, crop=crop,
                               suitability=suitability, fertilizer=fertilizer)

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
