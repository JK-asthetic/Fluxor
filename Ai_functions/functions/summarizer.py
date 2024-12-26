import json
import os
from collections import defaultdict
import pandas as pd
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx2txt import process as docx2txt_process

# Configure Gemini Pro API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_dir_summaries(paths: list):
    """
    Takes a list of directories and/or file paths and generates summaries in batch.
    """
    documents = []
    for path in paths:
        if os.path.isdir(path):
            documents.extend(process_directory(path))
        elif os.path.isfile(path):
            doc = process_single_file(path)
            if doc:
                documents.append(doc)

    if documents:
        summaries = batch_summarize_documents(documents)
        return summaries
    
    return []

def process_directory(dir_path: str):
    """
    Processes a directory and all its subdirectories to collect document content.
    """
    documents = []
    
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                doc = process_single_file(file_path, base_path=dir_path)
                if doc:
                    documents.append(doc)

    return documents

def extract_text_from_docx(docx_path):
    """Extract text from DOCX files using docx2txt."""
    try:
        text = docx2txt_process(docx_path)
        return text[:1000] if text else ""
    except Exception as e:
        print(f"Error reading DOCX file {docx_path}: {str(e)}")
        return ""

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF files."""
    reader = PdfReader(pdf_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
        if len(text) > 1000:
            break
    return text[:1000]

def process_single_file(path: str, base_path: str = None):
    """
    Processes a single file and returns a document object with its content and metadata.
    """
    try:
        relative_path = os.path.relpath(path, base_path) if base_path else path
        filename = os.path.basename(path)
        file_extension = os.path.splitext(filename)[1].lower()
        
        content = ""
        
        if file_extension == '.pdf':
            content = extract_text_from_pdf(path)
        elif file_extension == '.docx':
            content = extract_text_from_docx(path)
        elif file_extension in ['.txt', '.py']:
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()[:1000]
            except UnicodeDecodeError:
                # Try different encoding if utf-8 fails
                with open(path, 'r', encoding='latin-1') as file:
                    content = file.read()[:1000]
        elif file_extension in ['.xlsx', '.xls', '.xlsm']:
            try:
                df = pd.read_excel(path)
                content = df.to_string()[:1000]
            except Exception as e:
                print(f"Error reading Excel file {path}: {str(e)}")
                return None
        elif file_extension == '.csv':
            try:
                df = pd.read_csv(path)
                content = df.to_string()[:1000]
            except Exception as e:
                print(f"Error reading CSV file {path}: {str(e)}")
                return None
        else:
            print(f"Skipping unsupported file type: {filename}")
            return None

        # Clean and sanitize content for JSON
        content = content.replace('"', "'").replace('\n', ' ').strip()
        content = ' '.join(content.split())  # Normalize whitespace
        
        if not content:
            print(f"No content extracted from file: {filename}")
            return None

        return {
            "file_path": relative_path,
            "content": content
        }

    except Exception as e:
        print(f"Error processing file '{path}': {str(e)}")
        return None

def batch_summarize_documents(documents):
    model = genai.GenerativeModel('gemini-pro')

    """
    Summarizes multiple documents using Gemini Pro API in a single call.
    """
    prompt = """
    You will be provided with a list of documents containing file content and metadata. 
    Generate a summary for each document. The summaries should help organize files based on their content. 
    Make each summary concise but informative and specific to the file.

    Return the result in a JSON array where each object has the following schema:
    {
        "file_path": "path to the file including name",
        "summary": "summary of the content"
    }

    The response should maintain the same order as the input documents.
    Only return the JSON array without any additional text or explanation.
    """

    # Prepare the content for the API call
    formatted_docs = []
    for doc in documents:
        formatted_docs.append({
            "file_path": doc["file_path"],
            "content": doc["content"]
        })

    try:
        response = model.generate_content(prompt + "\n\n" + json.dumps(formatted_docs))
        response_text = response.text.strip()
        # Handle potential JSON formatting issues
        if not response_text.startswith('['):
            response_text = response_text[response_text.find('['):response_text.rfind(']')+1]
        
        summaries = json.loads(response_text)
        return summaries

    except Exception as e:
        print(f"Error in batch summarization: {str(e)}")
        return []

def truncate_cell(x, max_chars):
    """Truncate cell content if it exceeds max_chars."""
    x_str = str(x)
    return x_str[:max_chars] + '...' if len(x_str) > max_chars else x_str