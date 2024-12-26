
import os
import mimetypes
import shutil

def categorize_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)

    if mime_type:
        if mime_type.startswith('application'):
            if "msword" in mime_type or "vnd.openxmlformats" in mime_type:
                if file_path.endswith('.pptx'):
                    return "Presentations"  # Handle .pptx explicitly
                return "Documents"
            elif "excel" in mime_type or "spreadsheet" in mime_type:
                return "Spreadsheets"
            elif "presentation" in mime_type or file_path.endswith(('.ppt', '.pptx', '.odp')):
                return "Presentations"  # Handle .ppt and .odp as well
            elif mime_type == 'application/pdf':
                return "PDFs"
            elif mime_type in ('application/epub+zip', 'application/x-mobipocket-ebook'):
                return "eBooks"
            elif mime_type == 'application/rtf':
                return "Rich Text Documents"
            elif mime_type == 'application/vnd.oasis.opendocument.text':
                return "OpenDocument Text"
            elif mime_type == 'application/latex':
                return "LaTeX Documents"
            elif "x-font" in mime_type or mime_type == 'application/font-woff':
                return "Fonts"
            elif mime_type in ('application/json', 'application/xml', 'application/sql'):
                return "Data Formats"
            elif mime_type == 'application/java-archive':
                return "Java Archives"
            elif mime_type == 'application/octet-stream' and file_path.endswith(('.dll', '.so', '.dylib')):
                return "Libraries"
            elif file_path.endswith(('.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz')):
                return "Compressed Files"
            elif file_path.endswith(('.iso', '.img', '.dmg')):
                return "Disk Images"
            elif mime_type.startswith('application/x-executable') or file_path.endswith(('.exe', '.bat', '.sh', '.jar', '.msi')):
                return "Executables"
            else:
                return "Other Documents"
        
        # Images
        elif mime_type.startswith('image'):
            return "Images"
        
        # Audio
        elif mime_type.startswith('audio'):
            return "Audio"
        
        # Video
        elif mime_type.startswith('video'):
            return "Video"
        
        # Text and Code Files
        elif mime_type.startswith('text'):
            if file_path.endswith(('.py', '.js', '.html', '.css', '.csv', '.sh')):
                return "Code/Programming"
            return "Text Files"
        
        # Mobile Apps
        elif file_path.endswith(('.apk', '.ipa')):
            return "Mobile Apps"
        
        # Emails
        elif file_path.endswith(('.msg', '.eml')):
            return "Emails"
        
        # Calendar Files
        elif file_path.endswith('.ics'):
            return "Calendar Files"
        
        # Project Management Files
        elif file_path.endswith('.mpp'):
            return "Microsoft Project Files"
        elif file_path.endswith('.gan'):
            return "GanttProject Files"
    
    if file_path.endswith((
        '.py', '.java', '.class', '.c', '.cpp', '.cs', '.html', '.css', '.js', '.ts', 
        '.json', '.xml', '.sh', '.bat', '.r', '.php', '.pl', '.rb', '.go', '.swift', 
        '.scala', '.kt', '.kts', '.dart', '.rs', '.jl', '.ipynb', '.m', '.h')):
        return "Code/Programming"

    return "Others"

def organize_files(source_folder):
    items = os.listdir(source_folder)
    item_list = []
    for item in items:
        item_path = os.path.join(source_folder, item)
        
        if os.path.isdir(item_path):
            print(f"Skipping folder: {item}")
            continue
            
        if os.path.isfile(item_path):
            category = categorize_file(item_path)
            
            destination_folder = os.path.join(source_folder, category)
            
            
            destination_path = os.path.join(destination_folder, item)
            item_list.append([item_path, destination_path, destination_folder])
            try:
                # shutil.move(item_path, destination_path)
                print(f"Moved: {item} -> {category}")
            except Exception as e:
                print(f"Error moving {item}: {str(e)}")

    return item_list
