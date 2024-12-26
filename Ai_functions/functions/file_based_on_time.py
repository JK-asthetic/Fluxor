import os
import shutil
from datetime import datetime

def organize_files_by_date(source_folder, sort_by="year", use_created_date=True):
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            file_path = os.path.join(root, file)

            if use_created_date:
                file_time = os.path.getctime(file_path)  
            else:
                file_time = os.path.getmtime(file_path)  

            file_date = datetime.fromtimestamp(file_time)

            if sort_by == "year":
                folder = os.path.join(source_folder, str(file_date.year))
            elif sort_by == "month":
                folder = os.path.join(source_folder, str(file_date.year), file_date.strftime('%B'))
            elif sort_by == "day":
                folder = os.path.join(source_folder, str(file_date.year), file_date.strftime('%B'), file_date.strftime('%d'))
            elif sort_by == "date":
                folder = os.path.join(source_folder, file_date.strftime('%Y-%m-%d'))  # Folder named by date (YYYY-MM-DD)
            else:
                folder = os.path.join(source_folder, str(file_date.year))  # Default to year

            if not os.path.exists(folder):
                os.makedirs(folder)

            destination_path = os.path.join(folder, file)
            shutil.move(file_path, destination_path)
            print(f"Moved: {file} -> {folder}")

def main():
    source_folder = input("Enter the path to the folder containing the files: ")

    date_choice = input("Do you want to sort by creation date or modification date? (enter 'created' or 'modified'): ").lower()
    use_created_date = True if date_choice == "created" else False
    sort_choice = input("How would you like to sort the files? (enter 'year', 'month', 'day', 'date'): ").lower()
    organize_files_by_date(source_folder, sort_by=sort_choice, use_created_date=use_created_date)

if __name__ == "__main__":
    main()
