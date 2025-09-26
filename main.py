import os
from flask import Flask, render_template, request, Markup
import markdown
from soil_utils import parse_soil_report, gemini_soil_analysis

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files.get('file')
        crop = request.form.get('crop')
        if not file or file.filename == '':
            return "No file selected", 400
        if not crop:
            return "Please enter crop name", 400

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        soil_data = parse_soil_report(filepath)

        # Call Gemini API for rich analysis and get markdown text output
        analysis = gemini_soil_analysis(soil_data, crop)

        # Convert markdown text to safe HTML for rendering in template
        analysis_html = Markup(markdown.markdown(analysis))

        return render_template('index.html',
                               soil=soil_data,
                               crop=crop,
                               analysis=analysis_html)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
