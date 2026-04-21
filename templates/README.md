# ✧ AI Resume Parser | Executive Edition

An enterprise-grade, NLP-powered web application designed to automatically extract contact telemetry and technical proficiencies from unstructured PDF resumes.

## ✨ Intelligence Engine Features
* **Automated Data Extraction:** Seamlessly parses PDF documents utilizing `PyMuPDF` to strip raw text while handling complex visual layouts.
* **Named Entity Recognition (NER):** Powered by `spaCy`, the industry-standard NLP engine, to identify and categorize technical skills against a dynamic proficiency database.
* **Regex Architecture:** Utilizes advanced regular expressions to accurately isolate phone numbers and email addresses.
* **Premium UI/UX:** Features a glassmorphism dark-mode interface with asynchronous processing, golden accents, and micro-interaction animations.

## 🛠️ Tech Stack
* **Backend:** Python, Flask, Werkzeug
* **NLP & Processing:** spaCy, PyMuPDF (`fitz`), Regular Expressions (Regex)
* **Frontend:** HTML5, CSS3, Vanilla JavaScript (Fetch API)

## 🚀 Deployment Instructions
1. Clone the repository:
   ```bash
   git clone [https://github.com/Jaikrishna115/resume-parser.git](https://github.com/Jaikrishna115/resume-parser.git)


Install the necessary dependencies:

pip install -r requirements.txt
python -m spacy download en_core_web_sm


Boot the Flask server:
python app.py