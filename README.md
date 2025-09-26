# Soil Analysis AI Web Application

A Flask-based web application that analyzes soil test PDFs using Google Gemini AI to provide intelligent crop suitability analysis and fertilizer recommendations.

## Features

- Upload soil test reports in PDF format.
- Extract key soil parameters (pH, Nitrogen, Phosphorus, Potassium).
- Use Gemini AI for detailed soil and crop analysis.
- Display major conclusions and actionable fertilizer advice.
- Modern, responsive web UI for easy access on all devices.

## Project Structure

| File/Folder         | Description                                    |
|---------------------|------------------------------------------------|
| `main.py`           | Flask backend application entry point.        |
| `soil_utils.py`     | Soil report parsing and Gemini AI integration.|
| `requirements.txt`  | Python dependencies list.                       |
| `templates/`        | HTML templates, includes `index.html`.         |
| `static/`           | Static files: CSS styles (`style.css`).         |
| `uploads/`          | Directory created at runtime for uploaded PDFs. |
| `README.md`         | Project documentation and instructions.        |
| `lag_sample.pdf`    | Example soil test PDF for testing.              |

## Setup Instructions

### Prerequisites

- Python 3.9 or higher
- [Virtualenv](https://python.org/dev/peps/pep-0405/#virtualenvironments) recommended

### Installation

1. Clone this repository
2. Create and activate a virtual environment:

**On Windows:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set your Google Gemini API key as an environment variable:

**Windows PowerShell:**

```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

**macOS/Linux:**

```bash
export GEMINI_API_KEY="your_api_key_here"
```

## Running The Application

Start the Flask development server:

```bash
python main.py
```

Open your web browser and navigate to:

```
http://localhost:5000
```

Upload a soil PDF and enter the crop grown for analysis.

***

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to open a GitHub Issue or Pull Request.

***

## License

This project is licensed under the MIT License.

***

## Acknowledgments

- Flask Framework
- Google Gemini AI API
- PyPDF2 for PDF text extraction

***

Let me know if you want me to format this as a markdown file or add more deployment platform-specific instructions!
