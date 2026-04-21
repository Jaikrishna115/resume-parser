import fitz  # This is the PyMuPDF library

def extract_text_from_pdf(pdf_path):
    print(f"Attempting to read: {pdf_path}...\n")
    raw_text = ""
    
    try:
        # 1. Open the PDF document
        doc = fitz.open(pdf_path)
        
        # 2. Loop through every page in the document
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            
            # 3. Extract the text from the current page
            raw_text += page.get_text()
            
        return raw_text
        
    except Exception as e:
        return f"🚨 Error reading PDF: {e}"

# --- Let's test it! ---
if __name__ == "__main__":
    # Point this to your sample resume file
    file_name = "sample_resume.pdf" 
    
    # Run our function
    text_output = extract_text_from_pdf(file_name)
    
    print("--- RAW EXTRACTED TEXT ---")
    print(text_output)
    print("--------------------------")