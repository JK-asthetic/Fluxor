import os
import google.generativeai as genai
from PyPDF2 import PdfReader
import comtypes.client
import json
import pandas as pd

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# Extract text from DOCX
def extract_text_from_docx(docx_path):
    word = comtypes.client.CreateObject('Word.Application')
    word.Visible = False
    doc = word.Documents.Open(docx_path)
    doc_text = doc.Content.Text
    doc.Close(False)
    word.Quit()
    return doc_text[:1000]

# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
        if len(text) > 1000:
            break
    return text[:1000]

# Call Gemini API with file content
def analyze_content(contents):
    prompt = '''
    Analyze the following content and suggest concise, descriptive filenames (without extension) based on their main topics or purposes. 
    Return the result in the following JSON format for each file:
    {
        "previous_name": "previous_filename",
        "file_path": "path_to_the_file",
        "new_file_name": "suggested_filename with extention",
        "status": "Success" or "Unsuccessful"
    }

    Since Various file contents are provided it should be in list of the Json format in order of the file's provided.
    Only give the list and do not include any extra text.
    '''

    for file_content in contents:
        prompt += f'''
        {{
            "file_path": "{file_content['file_path']}",
            "content": "{file_content['content'][:1000]}"
        }},
        '''

    response = model.generate_content(prompt)
    return response.text.strip()



# Main function to process file paths and get recommended names
def get_recommended_names(paths: list):
    contents = []
    
    for file_info in paths:
        file_path = file_info["file_path"]
        
        if os.path.isfile(file_path):
            filename = os.path.basename(file_path)
            file_extension = os.path.splitext(filename)[1].lower()
            
            content = ""
            try:
                if file_extension == '.pdf':
                    content = extract_text_from_pdf(file_path)
                elif file_extension == '.docx':
                    content = extract_text_from_docx(file_path)
                elif file_extension == '.txt' or file_extension == '.py':
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()[:1000]
                elif file_extension == '.py':
                    try:
                        with open(file_path, 'r', encoding='utf-8') as file:
                            content = file.read()[:1000]  # Read first 1000 characters from the Python file
                    except Exception as e:
                        print(f"Error reading Python file: {e}")
                        continue
                elif file_extension == '.xlsx':
                    try:
                        df = pd.read_excel(file_path)
                        content = df.to_string()[:1000]  # Convert to string and limit the length
                    except Exception as e:
                        print(f"Error reading Excel file: {e}")
                        continue
                elif file_extension == '.csv':
                    try:
                        df = pd.read_csv(file_path)
                        content = df.to_string()[:1000]  # Convert to string and limit the length
                    except Exception as e:
                        print(f"Error reading CSV file: {e}")
                        continue
                else:
                    print(f"Skipping unsupported file type: {filename}")
                    continue
                
                contents.append({
                    "file_path": file_path,
                    "previous_name": filename,
                    "content": content
                })
            
            except Exception as e:
                print(f"Error processing file '{filename}': {str(e)}")

    if contents:
        try:
            api_response = analyze_content(contents)
            print(api_response)
            # Parse the API response into a list of dictionaries
            recommended_names = json.loads(api_response)
            
            return recommended_names
        
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error: {str(e)}")
            return []
    
    return []