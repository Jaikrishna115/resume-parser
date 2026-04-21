from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename

# Import your custom scripts!
from extractor import extract_text_from_pdf
from parser import parse_resume

app = Flask(__name__)

# Create a temporary folder for uploaded resumes
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # 1. Check if a file was sent
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    # 2. Process the PDF
    if file and file.filename.endswith('.pdf'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Step A: Extract raw text
            raw_text = extract_text_from_pdf(filepath)
            
            if raw_text.startswith("🚨"):
                return jsonify({'error': 'Could not read PDF'}), 500
                
            # Step B: Run the NLP parser
            parsed_data = parse_resume(raw_text)
            
            # Step C: Delete the temporary file
            os.remove(filepath)
            
            return jsonify(parsed_data)
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
            
    return jsonify({'error': 'Invalid file format. Please upload a PDF.'}), 400

if __name__ == '__main__':
    # We turn off the reloader here to prevent issues with the NLP model loading twice
    app.run(debug=True, use_reloader=False)