from qt_core import *
from gui.widgets.py_push_button import PyPushButton
from pathlib import Path
import os

class DirectoryContentsWidget(QWidget):

    def update_tree_widget_with_type(self, list_item):
        self.tree_widget.clear()

        # Extract all destination paths
        destination_paths = [Path(sublist[1]) for sublist in list_item]
        
        # Find the common base directory for all destination paths
        base_dir = os.path.commonpath(destination_paths)
        
        tree = {}
        
        # Populate the tree dictionary based on the destination path relative to the base directory
        for sublist in list_item:
            item_path = sublist[0]  # First element in the sublist is item_path
            destination_path = sublist[1]  # Second element is destination_path
            
            # Make the destination path relative to the base directory
            relative_dst_path = Path(destination_path).relative_to(base_dir)
            dst_path_parts = relative_dst_path.parts  # Split the relative destination path into parts
            
            current = tree
            for part in dst_path_parts:  # Traverse or create the tree for the relative path
                current = current.setdefault(part, {})
            
            # Mark the file with its source path (optional, for tracking)
            current['_item_path'] = item_path

        # Function to recursively add items to the QTreeWidget
        def add_items(parent_item, tree_data):
            for key, value in tree_data.items():
                if key == '_item_path':
                    continue  # Skip internal data used to track source paths
                
                # Add item to the tree widget
                item = QTreeWidgetItem(parent_item, [key, "Directory" if isinstance(value, dict) else "File"])
                
                # If it's a directory, call the function recursively
                if isinstance(value, dict):
                    add_items(item, value)

        # Add all items starting from the invisible root
        add_items(self.tree_widget.invisibleRootItem(), tree)


    def update_tree_widget_with_renaming(self, files, recommended_names):
        self.tree_widget.clear()  # Clear the tree widget for new data

        rec_names_dict = {rec_name_info.get("file_path", ""): rec_name_info for rec_name_info in recommended_names}

        for file_info in files:
            file_path = file_info["file_path"]
            previous_name = file_info["previous_name"]

            if file_path in rec_names_dict:
                rec_name_info = rec_names_dict[file_path]
                new_name = rec_name_info.get("new_file_name", previous_name)
                status = rec_name_info.get("status", "Unsuccessful")

                display_name = new_name if status == "Success" else previous_name

                item = QTreeWidgetItem([previous_name, display_name])
                self.tree_widget.addTopLevelItem(item)

    def get_all_files(self, selected_directory, inp_type):
        self.tree_widget.clear()
        files = []

        if inp_type == "dir":
            for root, dirs, filenames in os.walk(selected_directory):
                for filename in filenames:
                    file_path = Path(root) / filename  # Full file path
                    files.append({
                        "file_path": str(file_path),
                        "previous_name": filename
                    })
        elif inp_type == "file":
            for file_path in selected_directory:
                file_path = Path(file_path)  # Convert to Path object for consistency
                filename = file_path.name  # Get the filename from the path
                
                files.append({
                    "file_path": str(file_path),
                    "previous_name": filename
                })

        for file_info in files:
            item = QTreeWidgetItem([file_info["previous_name"], ""])  # Add to tree (you can add new names later)
            self.tree_widget.addTopLevelItem(item)

        return files

    # For ai file manager
    def update_directory_created(self, files, select_directory):
        self.tree_widget.clear()

        src_path = os.path.commonpath(select_directory)
        
        tree = {}
        for file in files:
            parts = Path(file["dst_path"]).parts  
            current = tree
            for part in parts:
                current = current.setdefault(part, {})
        def add_items(parent_item, tree_data):
            for key, value in tree_data.items():
                item = QTreeWidgetItem(parent_item, [key, "Directory" if isinstance(value, dict) else "File"])
                if isinstance(value, dict): 
                    add_items(item, value)

        add_items(self.tree_widget.invisibleRootItem(), tree)

    def update_directory_contents(self, path):
        self.tree_widget.clear()
        directory = Path(path)
        self.populate_tree(self.tree_widget.invisibleRootItem(), directory)

    def populate_tree(self, parent_item, directory):
        for path in sorted(directory.iterdir()):
            item = QTreeWidgetItem(parent_item, [path.name, "Directory" if path.is_dir() else "File"])
            if path.is_dir():
                self.populate_tree(item, path)
                
    def set_custom_headers(self, header_type="default"):
        """
        Sets the headers for the QTreeWidget.
        :param header_type: Can be 'default' for Name/Type or 'rename' for Previous Name/New Name.
        """
        if header_type == "default":
            self.tree_widget.setHeaderLabels(["Name", "Type"])
        elif header_type == "rename":
            self.tree_widget.setHeaderLabels(["Previous Name", "New Name"])

        header = self.tree_widget.header()
        header.setSectionResizeMode(QHeaderView.Stretch)




    def __init__(
        self,
        radius = 8,
        color = "#FFF",
        bg_color = "#444",
        selection_color = "#FFF",
        header_horizontal_color = "#333",
        header_vertical_color = "#444",
        bottom_line_color = "#555",
        grid_line_color = "#555",
        scroll_bar_bg_color = "#FFF",
        scroll_bar_btn_color = "#3333",
        context_color = "#00ABE8"
    ):  
        super().__init__()

        # PROPERTIES
        self.color = color
        self.bg_color = bg_color
        self.selection_color = selection_color
        self.header_horizontal_color = header_horizontal_color
        self.header_vertical_color = header_vertical_color
        self.bottom_line_color = bottom_line_color
        self.grid_line_color = grid_line_color
        self.scroll_bar_bg_color = scroll_bar_bg_color
        self.scroll_bar_btn_color = scroll_bar_btn_color
        self.context_color = context_color

        # SETUP WIDGET
        self.setObjectName("directory_contents_widget")
        self.setStyleSheet(f'''
        #directory_contents_widget {{
            background-color: {bg_color};
            border-radius: {radius}px;
            border: none;
        }}
        QTreeWidget {{
            background-color: {bg_color};
            border: 3px solid {header_horizontal_color};
            color: {color};
            border-radius: {radius}px;
        }}
        QTreeWidget::item:selected {{
            background-color: {selection_color};
        }}
        QHeaderView::section {{
            background-color: {header_horizontal_color};
            color: {color};
            border: none;
            padding: 5px;
        }}
        QHeaderView::section:horizontal {{
            border-top: 1px solid {bottom_line_color};
        }}
        QHeaderView::section:vertical {{
            border-left: 1px solid {header_vertical_color};
        }}
        QScrollBar:horizontal {{
            border: none;
            background: {scroll_bar_bg_color};
            height: 8px;
            margin: 0px 21px 0 21px;
            border-radius: 4px;
        }}
        QScrollBar::handle:horizontal {{
            background: {scroll_bar_btn_color};
            min-width: 25px;
            border-radius: 4px
        }}
        QScrollBar:vertical {{
            border: none;
            background: {scroll_bar_bg_color};
            width: 8px;
            margin: 21px 0 21px 0;
            border-radius: 4px;
        }}
        QScrollBar::handle:vertical {{
            background: {scroll_bar_btn_color};
            min-height: 25px;
            border-radius: 4px
        }}
        ''')

        # CREATE LAYOUT
        self.directory_layout = QVBoxLayout(self)
        self.directory_layout.setContentsMargins(0,0,0,0)

        # CREATE TREE WIDGET
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(["Name", "Type"])
        self.tree_widget.setColumnWidth(0, 300)
        self.tree_widget.setAnimated(True)
        self.tree_widget.setIndentation(20)
        self.tree_widget.setSortingEnabled(True)

        # ADD TREE WIDGET TO LAYOUT
        self.directory_layout.addWidget(self.tree_widget)