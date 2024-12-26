from groq import Groq
import json
import os

FILE_PROMPT = """
You will be provided with a list of source files and a summary of their contents. For each file, propose a new path and filename, using a directory structure that optimally organizes the files using known conventions and best practices.
Follow good naming conventions. Here are a few guidelines:
- Think about your files: What related files are you working with?
- Identify metadata (e.g., date, sample, experiment): What information is needed to easily locate a specific file?
- Abbreviate or encode metadata
- Use versioning: Are you maintaining different versions of the same file?
- Think about how you will search for your files: What comes first?
- Deliberately separate metadata elements: Avoid spaces or special characters in your file names

If the file is already named well or matches a known convention, set the destination path to the same as the source path.

If the user provides input for sorting preferences, follow those instructions for directory structure.
Your response must be a JSON object with the following schema:
```json
{
    "files": [
        {
            "src_path": "original file path",
            "dst_path": "new file path under proposed directory structure with proposed file name"
        }
    ]
}
""".strip()

def get_user_input(): 
    """Ask the user for input on how they would like the files organized.""" 
    user_input = input('''Please provide any specific directory structure or 
                       sorting method you'd prefer (or press Enter to skip): ''') 
    return user_input

def create_file_tree(summaries: list, user_sorting_input = ""): 
    client = Groq(api_key=os.getenv("GROG_API_KEY"))

    if user_sorting_input:
        system_prompt = f"{FILE_PROMPT}\n\nUser preferences: {user_sorting_input}"
    else:
        system_prompt = FILE_PROMPT

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps(summaries)},
        ],
        model="llama-3.1-70b-versatile",
        response_format={"type": "json_object"},  
        temperature=0,
    )

    file_tree = json.loads(chat_completion.choices[0].message.content)["files"]
    return file_tree
