
# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
from gui.uis.windows.main_window.functions_main_window import *
import sys
import os
from pathlib import Path
from Ai_functions.functions.summarizer import get_dir_summaries
from Ai_functions.functions.classifier import create_file_tree
from Ai_functions.functions.renaming import get_recommended_names
from Ai_functions.functions.file_based_on_type import organize_files
from Ai_functions.functions.chatbot import FluxorChatbot
from gui.widgets.Loader.py_loader import CircularLoader
from asciitree import LeftAligned
from asciitree.drawing import BoxStyle, BOX_LIGHT
from pathlib import Path
import click
import shutil



# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
from gui.core.json_settings import Settings

# IMPORT PY ONE DARK WINDOWS
# ///////////////////////////////////////////////////////////////
# MAIN WINDOW
from gui.uis.windows.main_window import *

# IMPORT PY ONE DARK WIDGETS
# ///////////////////////////////////////////////////////////////
from gui.widgets import *

# ADJUST QT FONT DPI FOR HIGHT SCALE AN 4K MONITOR
# ///////////////////////////////////////////////////////////////
os.environ["QT_FONT_DPI"] = "96"
# IF IS 4K MONITOR ENABLE 'os.environ["QT_SCALE_FACTOR"] = "2"'

class RecommendedNamesWorker(QThread):
    finished = Signal(list)  # Signal to emit recommended names
    error = Signal(str)      # Signal for error handling

    def __init__(self, files):
        super().__init__()
        self.files = files

    def run(self):
        try:
            recommended_names = get_recommended_names(self.files)
            self.finished.emit(recommended_names)
        except Exception as e:
            self.error.emit(str(e))


class FileRenamingWorker(QThread):
    finished = Signal()  # Signal when renaming is complete
    progress = Signal(str, str)  # Signal for each file renamed (old_name, new_name)
    error = Signal(str)  # Signal for error handling

    def __init__(self, rename_data):
        super().__init__()
        self.rename_data = rename_data

    def run(self):
        try:
            for item in self.rename_data:
                file_path = item["file_path"]
                new_filename = item["new_file_name"]
                filename = item["previous_name"]
                new_file_path = os.path.join(os.path.dirname(file_path), new_filename)
                
                os.rename(file_path, new_file_path)
                self.progress.emit(filename, new_filename)
            
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))


class DirectorySummaryWorker(QThread):
    finished = Signal(list)  # Signal to emit when processing is complete
    error = Signal(str)      # Signal to emit if an error occurs
    progress = Signal(int)   # Signal to emit progress updates

    def __init__(self, directory):
        super().__init__()
        self.directory = directory

    def run(self):
        try:
            # Call your existing function
            summaries = get_dir_summaries(self.directory)
            self.finished.emit(summaries)
        except Exception as e:
            self.error.emit(str(e))


class FileTreeWorker(QThread):
    finished = Signal(list)  # Signal to emit when processing is complete
    error = Signal(str)      # Signal to emit if an error occurs

    def __init__(self, summaries, user_sorting_input):
        super().__init__()
        self.summaries = summaries
        self.user_sorting_input = user_sorting_input

    def run(self):
        try:
            # Call your existing function
            classified = create_file_tree(self.summaries, user_sorting_input=self.user_sorting_input)
            self.finished.emit(classified)
        except Exception as e:
            self.error.emit(str(e))

class Worker(QObject):
    finished = Signal(str)  # Emit the AI response
    error = Signal(str)     # Emit errors
    
    def __init__(self, user_query: str, file_path: str):
        super().__init__()
        self.user_query = user_query
        self.file_path = file_path

    def run(self):
        try:
            fluxor = FluxorChatbot()
            fluxor.set_file_content(self.file_path)

            response = fluxor.chat(self.user_query)

            self.finished.emit(response)
        except Exception as e:
            self.error.emit(str(e))



# MAIN WINDOW
# ///////////////////////////////////////////////////////////////
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items

        # SETUP MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.hide_grips = True # Show/Hide resize grips
        SetupMainWindow.setup_gui(self)

        self.directory_worker = None
        self.tree_worker = None
        self.summaries = None
        self.names_worker = None
        self.rename_worker = None

        self.is_processing = False
        
        self.loader = CircularLoader(self)
        self.loader.hide()
        # Position loader in the center of the main window
        self.loader.move(
            self.width() // 2 - self.loader.width() // 2,
            self.height() // 2 - self.loader.height() // 2
        )

        # SHOW MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.show()


    # For ai file classifier
    # ///////////////////////////////////////////////////////////////

    def select_directory(self):
        
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)  # Set to directory selection mode
        dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)  # Show only directories, no files
        dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
        dialog.setDirectory(str(Path.home()))  # Set to user's home directory or change to a base path

        if dialog.exec():
            selected_directories = dialog.selectedFiles()  
            self.select_directory_dir = selected_directories
            print("Selected Directories:", selected_directories)
            self.directory_contents.update_directory_contents(selected_directories[0])


    def handle_implement_button(self):
        """This method is triggered when the 'Implement' button is pressed."""
        
        if len(self.clssifed_dir) == 0:
            print("Please Process the Directory first")
            return

        BASE_DIR = Path(self.select_directory_dir[0])  # Ensure this is a single string path

        for file in self.clssifed_dir:
            src_file_path = BASE_DIR / Path(file["src_path"])  # Add BASE_DIR to source path
            dst_file_path = BASE_DIR / Path(file["dst_path"])
            
            try:
                dst_file_path.parent.mkdir(parents=True, exist_ok=True)
                
                shutil.move(src_file_path, dst_file_path)
                print(f"Moved: {src_file_path} -> {dst_file_path}")
            except FileNotFoundError:
                print(f"Error: Source file not found - {src_file_path}")
            except PermissionError:
                print(f"Error: Permission denied when moving {src_file_path}")
            except Exception as e:
                print(f"Error moving {src_file_path}: {str(e)}")

        print("File moving process completed.")


    def classify_execute(self):
        user_text = self.line_edit.text()
        if len(self.select_directory_dir) == 0:
            print("Please select a directory or file")
            return

        # Show loader and set processing flag
        self.loader.setText("Loading ... ")
        self.loader.show()
        self.loader.start()
        self.is_processing = True

        # Start the directory summary worker
        self.directory_worker = DirectorySummaryWorker(self.select_directory_dir)
        self.directory_worker.finished.connect(self.on_summaries_complete)
        self.directory_worker.error.connect(self.on_worker_error)
        self.directory_worker.start()

    def on_summaries_complete(self, summaries):
        self.summaries = summaries
        self.loader.setText("Classifying Files...")
        
        # Start the classification worker
        self.tree_worker = FileTreeWorker(summaries, self.line_edit.text())
        self.tree_worker.finished.connect(self.on_classification_complete)
        self.tree_worker.error.connect(self.on_worker_error)
        self.tree_worker.start()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Keep loader centered when window is resized
        if hasattr(self, 'loader'):
            self.loader.move(
                self.width() // 2 - self.loader.width() // 2,
                self.height() // 2 - self.loader.height() // 2
            )

    def on_classification_complete(self, classified):
        self.loader.stop()
        self.loader.hide()  # Hide loader when done
        self.is_processing = False  # Reset processing flag

        self.proceesed_directory_contents.update_directory_created(classified, self.select_directory_dir)
        self.clssifed_dir = classified


    def on_worker_error(self, error_message):
        self.loader.stop()
        self.loader.hide()  # Hide loader on error
        self.is_processing = False  # Reset processing flag
        print(f"Error occurred: {error_message}")

    def closeEvent(self, event):
        # Stop loader if it's running
        if hasattr(self, 'loader'):
            self.loader.stop()
            
        # Clean up threads
        if self.directory_worker and self.directory_worker.isRunning():
            self.directory_worker.terminate()
            self.directory_worker.wait()
        if self.tree_worker and self.tree_worker.isRunning():
            self.tree_worker.terminate()
            self.tree_worker.wait()
        super().closeEvent(event)
    


    # AI File Reaniming   
    # /////////////////////////////////////////////////////////////////
    def rename_files(self):
        files = self.get_files
        
        # Create and start the recommended names worker
        self.names_worker = RecommendedNamesWorker(files)
        self.names_worker.finished.connect(self.on_names_received)
        self.names_worker.error.connect(self.on_worker_error)
        self.names_worker.start()

    def implement_renaming(self):
        # Create and start the renaming worker
        self.rename_worker = FileRenamingWorker(self.new_names_json)
        self.rename_worker.finished.connect(self.on_renaming_complete)
        self.rename_worker.progress.connect(self.on_file_renamed)
        self.rename_worker.error.connect(self.on_worker_error)
        self.rename_worker.start()

    def on_names_received(self, recommended_names):
        self.new_names_json = recommended_names
        self.name_comaprision.update_tree_widget_with_renaming(self.get_files, recommended_names)

    def on_renaming_complete(self):
        print("File renaming process completed successfully.")

    def on_file_renamed(self, old_name, new_name):
        print(f"Renamed '{old_name}' to '{new_name}'")

    def on_worker_error(self, error_message):
        print(f"Error occurred: {error_message}")
        QMessageBox.critical(self, "Error", error_message)


    def select_directory_page3(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)
        dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
        dialog.setDirectory(str(Path.home()))

        if dialog.exec():
            selected_directories = dialog.selectedFiles()  
            self.select_directory_dir = selected_directories
            print("Selected Directories:", selected_directories)
            self.get_files = self.name_comaprision.get_all_files(selected_directories[0], "dir")

    
    def select_file_page3(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)  
        dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
        dialog.setDirectory(str(Path.home()))  

        if dialog.exec():
            selected_files = dialog.selectedFiles()  
            self.select_directory_dir = selected_files 
            print("Selected Files:", selected_files)
            self.get_files = self.name_comaprision.get_all_files(selected_files, "file")

    def closeEvent(self, event):
        # Clean up any running threads before closing
        for worker in [self.names_worker, self.rename_worker]:
            if worker and worker.isRunning():
                worker.terminate()
                worker.wait()
        super().closeEvent(event)

    # File Sorting Based on Content
    # ///////////////////////////////////////////////////////////////
    def select_directory_page4(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)  # Set to directory selection mode
        dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)  # Show only directories, no files
        dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
        dialog.setDirectory(str(Path.home()))  # Set to user's home directory or change to a base path

        if dialog.exec():
            selected_directories_4 = dialog.selectedFiles()  
            self.selected_dir_page4 = selected_directories_4
            print("Selected Directories:", selected_directories_4)
            self.page4_show_dir.update_directory_contents(selected_directories_4[0])

    def execute_Sort_files_type(self):
        dir_selected = self.selected_dir_page4[0]
        item_list = organize_files(dir_selected)
        self.item_list_main = item_list
        self.page4_show_dir_2.update_tree_widget_with_type(item_list)


    def implement_sort_file_type(self):
        for i in self.item_list_main:
            destination_folder = i[2]
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)
            shutil.move(i[0], i[1])


    # page5 AI chatbot

    def select_directory_page5(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setOption(QFileDialog.Option.ShowDirsOnly, False)
        dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
        dialog.setDirectory(str(Path.home()))

        if dialog.exec():
            selected_files = dialog.selectedFiles()
            if selected_files:
                self.selected_file_path = selected_files[0]  # Store the selected file path
                print("Selected File:", self.selected_file_path)
    
    def add_chat_message(self, message: str, sender: str):
        message_layout = QHBoxLayout()
        icon_label = QLabel()
        if sender == "user":
            message_style = """
            background-color: #dcdcdc;
            font-size:18px;
            color: black;
            border-radius: 10px;
            padding: 6px;
            max-width: 800px;  /* Limit message width */
        """
            icon_pixmap = QPixmap(r"C:\Users\jatin\Desktop\Current Projects\Main Fluxor\Main-app\gui\images\user.ico").scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        else:  # sender == "ai"
            icon_pixmap = QPixmap(r"C:\Users\jatin\Desktop\Current Projects\Main Fluxor\Main-app\floxor.ico").scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            message_style = """
            font-size:18px;
            background-color: #dcdcdc;
            color: black;
            border-radius: 10px;
            padding: 6px;
            margin-right: 50px;  /* Offset for the icon */
            max-width: 800px;  /* Limit message width */
        """
        icon_label.setPixmap(icon_pixmap)
        icon_label.setStyleSheet("border: none; background: transparent; padding: 0px; margin: 6px;")


        # Add the icon to the layout
        message_layout.addWidget(icon_label)

        # Add the message text
        message_label = QLabel(message)
        message_label.setWordWrap(True)
        message_label.setStyleSheet(message_style)
        message_layout.addWidget(message_label)

        # Align messages differently for user and AI
        if sender == "user":
            message_layout.setAlignment(Qt.AlignRight)
        else:
            message_layout.setAlignment(Qt.AlignLeft)

        # Add the layout to the chat layout
        self.ui.load_pages.chat_layout.addLayout(message_layout)

    def send_message(self):
        user_text = self.ui.load_pages.user_text_input.text()
        if user_text.strip():
            # Add user message to the chat
            self.add_chat_message(user_text, "user")

            if not hasattr(self, "selected_file_path"):
                self.add_chat_message("No directory selected. Please select a directory first.", "ai")
                return

            # Create and start a thread
            self.thread = QThread()
            self.worker = Worker(user_text, self.selected_file_path)
            self.worker.moveToThread(self.thread)

            # Connect signals and slots
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.handle_ai_response)
            self.worker.error.connect(self.handle_error)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)

            # Start the thread
            self.thread.start()

            # Disable the input and send button while processing
            self.ui.load_pages.user_text_input.setDisabled(True)
            self.ui.load_pages.send_button.setDisabled(True)

            # Re-enable them when the thread finishes
            self.thread.finished.connect(lambda: self.ui.load_pages.user_text_input.setDisabled(False))
            self.thread.finished.connect(lambda: self.ui.load_pages.send_button.setDisabled(False))

    def handle_ai_response(self, response: str):
        self.add_chat_message(response, "ai")

    # Handle errors
    def handle_error(self, error: str):
        self.add_chat_message(error, "ai")



    # ///////////////////////////////////////////////////////////////
    def btn_clicked(self):
        btn = SetupMainWindow.setup_btns(self)

        # Remove selection if clicked by "btn_close_left_column"
        if btn.objectName() != "btn_settings":
            self.ui.left_menu.deselect_all_tab()


        # HOME BTN
        if btn.objectName() == "btn_home":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page 1
            MainFunctions.set_page(self, self.ui.load_pages.page_1)

            
        # Page-specific behavior
        if btn.objectName() == "File_Classify":
            # Check if still processing, show loader if true
            if self.is_processing:
                self.loader.show()

            self.ui.left_menu.select_only_one(btn.objectName())
            MainFunctions.set_page(self, self.ui.load_pages.page_2)
        
        # Handle other pages
        else:
            # Ensure loader is hidden when switching to any other page
            if self.loader.isVisible():
                self.loader.hide()
        # LOAD USER PAGE
        if btn.objectName() == "rename_file":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())
            # Load Page 3
            MainFunctions.set_page(self, self.ui.load_pages.page_3)

        # Page 4
        if btn.objectName() == "Segement_Files":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())
            # Load Page 4
            MainFunctions.set_page(self, self.ui.load_pages.page_4)

        # Page 5
        if btn.objectName() == "chat_bot":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())
            # Load Page 5
            MainFunctions.set_page(self, self.ui.load_pages.page_5)    

    
        # BOTTOM INFORMATION
        if btn.objectName() == "btn_info":
            # CHECK IF LEFT COLUMN IS VISIBLE
            if not MainFunctions.left_column_is_visible(self):
                self.ui.left_menu.select_only_one_tab(btn.objectName())

                # Show / Hide
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                if btn.objectName() == "btn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    # Show / Hide
                    MainFunctions.toggle_left_column(self)
                
                self.ui.left_menu.select_only_one_tab(btn.objectName())

            # Change Left Column Menu
            if btn.objectName() != "btn_close_left_column":
                MainFunctions.set_left_column_menu(
                    self, 
                    menu = self.ui.left_column.menus.menu_2,
                    title = "Info tab",
                    icon_path = Functions.set_svg_icon("icon_info.svg")
                )
    

        # SETTINGS LEFT
        if btn.objectName() == "btn_settings" or btn.objectName() == "btn_close_left_column":
            # CHECK IF LEFT COLUMN IS VISIBLE
            if not MainFunctions.left_column_is_visible(self):
                # Show / Hide
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                if btn.objectName() == "btn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    # Show / Hide
                    MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())

            # Change Left Column Menu
            if btn.objectName() != "btn_close_left_column":
                MainFunctions.set_left_column_menu(
                    self, 
                    menu = self.ui.left_column.menus.menu_1,
                    title = "Settings Left Column",
                    icon_path = Functions.set_svg_icon("icon_settings.svg")
                )
        
        # TITLE BAR MENU
        # ///////////////////////////////////////////////////////////////
        
        # SETTINGS TITLE BAR
        if btn.objectName() == "btn_top_settings":
            # Toogle Active
            if not MainFunctions.right_column_is_visible(self):
                btn.set_active(True)

                # Show / Hide
                MainFunctions.toggle_right_column(self)
            else:
                btn.set_active(False)

                # Show / Hide
                MainFunctions.toggle_right_column(self)

            # Get Left Menu Btn            
            top_settings = MainFunctions.get_left_menu_btn(self, "btn_settings")
            top_settings.set_active_tab(False)            

        # DEBUG
        print(f"Button {btn.objectName()}, clicked!")

        

    # LEFT MENU BTN IS RELEASED
    # Run function when btn is released
    # Check funtion by object name / btn_id
    # ///////////////////////////////////////////////////////////////
    def btn_released(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        # DEBUG
        print(f"Button {btn.objectName()}, released!")


    # RESIZE EVENT
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        SetupMainWindow.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

    


# SETTINGS WHEN TO START

# Set the initial class and also additional parameters of the "QApplication" class
# ///////////////////////////////////////////////////////////////
if __name__ == "__main__":
    # APPLICATION
    # ///////////////////////////////////////////////////////////////
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("floxor.ico"))
    window = MainWindow()

    # EXEC APP
    # ///////////////////////////////////////////////////////////////
    sys.exit(app.exec_())