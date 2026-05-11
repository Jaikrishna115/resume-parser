import os
import requests
import re
from dotenv import load_dotenv
from extractor import extract_text_from_pdf # Imports your previous script!

# 1. Load the pre-trained English NLP model
print("Loading NLP Model (this takes a second)...")
nlp = spacy.load("en_core_web_sm")

def generate_ai_summary(text):
    """
    Calls OpenRouter API to generate a 2-sentence executive summary.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    print(f"\n--- DEBUG: First 15 chars of key --- \n{str(api_key)[:15]}...\n")
    
    if not api_key or api_key == "sk-or-v1-your-actual-api-key-goes-here":
        return "AI Summary unavailable: Missing or invalid OPENROUTER_API_KEY in .env file."

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:5000", # OpenRouter recommends passing your site URL
                "X-Title": "Executive Resume Parser"     # OpenRouter recommends passing your app name
            },
            json={
                "model": "meta-llama/llama-3.1-8b-instruct:free",
                "temperature": 0.0, # Temperature 0 = No hallucinating/guessing
                "messages": [
                    {
                        "role": "system", 
                        "content": """You are a strict Data Extraction AI. 
                        Read the resume text and extract the candidate's professional summary and technical skills.

                        CRITICAL RULES:
                        1. NEVER guess or invent years of experience. Only mention years of experience if it is explicitly stated in the resume. 
                        2. If years of experience are not mentioned, simply provide a 2-sentence summary of the candidate's primary expertise and background based ONLY on what you understand from the text.
                        3. Extract ONLY actual technical skills, programming languages, and frameworks. Do not extract timeframes, project names, or soft skills.

                        Return your response STRICTLY as a JSON object without markdown formatting, formatted exactly like this:
                        {
                            "summary": "Exactly 2 professional sentences summarizing the resume.",
                            "skills": ["Skill 1", "Skill 2", "Skill 3"]
            }"""
                    },
                    {
                        "role": "user", 
                        "content": text
                    }
                ]
            },
            timeout=15 # Prevents your Flask app from freezing if the API is slow
        )
        
        if response.status_code == 200:
            data = response.json()
            raw_summary = data['choices'][0]['message']['content'].strip()
            
            # Clean up chatty LLM introductions and bold formatting
            # Clean up chatty LLM introductions AND the "**Summary:**" tag
            clean_summary = re.sub(r'^(?:Here is a summary.*?:\s*)?(?:\*?\*?Summary:\*?\*?\s*)?', '', raw_summary, flags=re.IGNORECASE|re.DOTALL)
            
            return clean_summary.strip()
        else:
            print(f"OpenRouter Error: {response.text}") # Logs the exact error to your terminal
            return f"AI Summary failed: API returned status {response.status_code}."
            
    except Exception as e:
        return f"AI Summary error: Connection failed."

def parse_resume(text):
    # Pass the text into the NLP engine
    doc = nlp(text)
    
    # Initialize our structured data dictionary
    parsed_data = {
        "email": None,
        "phone": None,
        "skills": []
    }

    # 2. Extract Email using Regular Expressions (Regex)
    # This looks for standard email formats (text@text.com)
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    if emails:
        parsed_data["email"] = emails[0]

    # 3. Extract Phone Number using Regex
    # This looks for numbers like +91 9100692965 or standard 10 digit numbers
    phone_pattern = r'\+?\d{2,3}[\s-]?\d{10}'
    phones = re.findall(phone_pattern, text.replace(" ", "")) # Removing spaces helps regex catch formatting quirks
    if phones:
        parsed_data["phone"] = phones[0]
        
    url_pattern = r'(https?://(?:www\.)?(?:linkedin\.com|github\.com)/[a-zA-Z0-9_-]+)'
    links = re.findall(url_pattern, text.lower())
    if links:
        parsed_data["links"] = list(set(links))
        
    # Generate Executive Summary (Passing the first 2500 characters to keep API costs/latency low)
    parsed_data["summary"] = generate_ai_summary(text[:5000])

    # 4. Extract Skills using NLP token matching
    # A standard parser checks against a massive database of thousands of skills.
    # We use a set {} here because it makes the keyword lookup lightning fast
    tech_stack = {
        # Programming Languages
        "python", "java", "javascript", "typescript", "c", "cpp", "c++", "c#", "ruby", 
        "php", "swift", "kotlin", "go", "golang", "rust", "r", "matlab", "bash", "shell", 
        "dart", "scala", "perl", "haskell",
        
        # Data Science, AI & Machine Learning
        "pandas", "numpy", "matplotlib", "seaborn", "scikit-learn", "tensorflow", 
        "keras", "pytorch", "opencv", "nltk", "spacy", "transformers", "langchain", 
        "faiss", "xgboost", "lightgbm", "llm", "llama", "nlp", "yolo", "scipy", 
        "jupyter", "colab", "databricks", "huggingface",
        
        # Web & App Development
        "html", "css", "react", "angular", "vue", "node", "nodejs", "express", 
        "django", "flask", "fastapi", "spring", "springboot", "bootstrap", 
        "tailwind", "jquery", "sass", "less", "nextjs", "reactnative", "flutter",
        
        # Databases & Storage
        "sql", "mysql", "postgresql", "postgres", "mongodb", "sqlite", "redis", 
        "cassandra", "oracle", "dynamodb", "neo4j", "firebase", "supabase", 
        "elasticsearch", "mariadb", "couchdb",
        
        # Cloud, Infrastructure & DevOps
        "aws", "azure", "gcp", "docker", "kubernetes", "k8s", "jenkins", "git", 
        "github", "gitlab", "bitbucket", "terraform", "ansible", "linux", "ubuntu", 
        "centos", "unix", "nginx", "apache", "docker-compose",
        
        # Big Data & Analytics
        "hadoop", "spark", "pyspark", "kafka", "tableau", "powerbi", "excel", 
        "snowflake", "airflow", "bigquery",
        
        # Tools & Methodologies
        "agile", "scrum", "jira", "confluence", "figma", "postman", "swagger", 
        "rest", "graphql", "json", "xml", "pytest", "selenium"
    }
    
    found_skills = set() # We use a 'set' to avoid duplicate skills
    
    # The NLP engine breaks the document into individual words (tokens)
    for token in doc:
        # Check if the word is in our tech stack database
        if token.text.lower() in tech_stack:
            found_skills.add(token.text.capitalize())
            
    parsed_data["skills"] = list(found_skills)
    
    return parsed_data

if __name__ == "__main__":
    file_name = "sample_resume.pdf"
    
    # Step 1: Extract the raw text using your first file
    raw_text = extract_text_from_pdf(file_name)
    
    # Step 2: Parse the structured data using this file
    if not raw_text.startswith("🚨"):
        print("\n--- PARSED RESUME DATA ---")
        structured_data = parse_resume(raw_text)
        
        for key, value in structured_data.items():
            print(f"{key.upper()}: {value}")
        print("--------------------------")
