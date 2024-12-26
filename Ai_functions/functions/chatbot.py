import os
import PyPDF2
import csv
import google.generativeai as genai
from dotenv import load_dotenv

# Configure the Gemini API
load_dotenv()   
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to extract text from PDF files
def process_pdf(file_path):
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ''.join([page.extract_text() for page in reader.pages])
        return text
    except Exception as e:
        print(f"Error processing PDF file: {e}")
        return None


# Function to extract text from CSV files
def process_csv(file_path):
    try:
        rows = []
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append(', '.join(row))
        return '\n'.join(rows)
    except Exception as e:
        print(f"Error processing CSV file: {e}")
        return None

# Function to extract text based on file type
def extract_text(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension == ".pdf":
        return process_pdf(file_path)
    elif file_extension == ".csv":
        return process_csv(file_path)
    else:
        print(f"Unsupported file format: {file_extension}")
        return None

# Chatbot logic
class FluxorChatbot:
    def __init__(self):
        self.conversation_history = []
        self.file_content = None
        self.generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=self.generation_config,
            system_instruction="You are Fluxor, an AI Chatbot. Help users with their file content and queries.",
        )

    def set_file_content(self, file_path):  
        self.file_content = extract_text(file_path)

    def chat(self, user_query):
        if not self.file_content:
            return "No file content available. Please upload a file first."

        # Add user query to the conversation history
        self.conversation_history.append({
            "role": "user",
            "parts": [
                self.file_content,
                user_query,
            ],
        })

        # Start a chat session
        try:
            chat_session = self.model.start_chat(history=self.conversation_history)
            response = chat_session.send_message(user_query)

            # Add AI response to the conversation history
            self.conversation_history.append({
                "role": "model",
                "parts": [response.text],
            })
            return response.text
        except Exception as e:
            print(f"Error interacting with the AI model: {e}")
            return "Error processing your request."
