✧ AI Resume Parser | Executive Edition
An enterprise-grade, NLP-powered web application designed to automatically extract contact telemetry and technical proficiencies from unstructured PDF resumes.

✨ Intelligence Engine Features
Automated Data Extraction: Seamlessly parses PDF documents utilizing PyMuPDF for rapid, secure raw text extraction.

Exhaustive Proficiency Matching: Powered by spaCy tokenization, the engine evaluates candidate text against a massive "Mega-Dictionary" of modern tech stacks to guarantee high-precision skill extraction without AI hallucination.

Regex Architecture: Utilizes advanced regular expressions to accurately isolate phone numbers and email addresses, accounting for regional formatting variances.

Premium UI/UX: Features a glassmorphism dark-mode interface with asynchronous processing, golden accents, drag-and-drop capabilities, and micro-interaction animations.

🛠️ Tech Stack
Backend: Python, Flask, Werkzeug

NLP & Processing: spaCy (en_core_web_sm), PyMuPDF (fitz), Regular Expressions (Regex)

Frontend: HTML5, CSS3, Vanilla JavaScript (Fetch API)

📁 Project Structure
Plaintext
resume-parser/
├── app.py              # Flask server and API routing
├── extractor.py        # PyMuPDF text extraction logic
├── parser.py           # spaCy NLP processing and Regex engine
├── requirements.txt    # Python dependencies
└── templates/
    └── index.html      # Premium glassmorphism frontend
🚀 Deployment Instructions
1. Clone the repository:

Bash
git clone https://github.com/Jaikrishna115/resume-parser.git
cd resume-parser

2. Install the necessary dependencies:

pip install -r requirements.txt

3. Download the NLP core model:

python -m spacy download en_core_web_sm

4. Boot the Intelligence Engine:

python app.py
The application will be available locally at http://127.0.0.1:5000

💡 Usage
Open the web interface in your browser.

Drag and drop a candidate's PDF resume into the upload zone.

Click Execute Extraction.

The engine will process the document asynchronously and display the parsed telemetry (Email, Phone, Skills) in a clean, animated results grid.