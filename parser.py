import spacy
import re
from extractor import extract_text_from_pdf # Imports your previous script!

# 1. Load the pre-trained English NLP model
print("Loading NLP Model (this takes a second)...")
nlp = spacy.load("en_core_web_sm")

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