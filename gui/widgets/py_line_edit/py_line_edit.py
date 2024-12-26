# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# STYLE
# ///////////////////////////////////////////////////////////////
style = '''
QLineEdit {{
    background-color: {_bg_color};
    border-radius: {_radius}px;
    border: {_border_size}px solid transparent;
    padding-left: 10px;
    padding-right: 10px;
    selection-color: {_selection_color};
    selection-background-color: {_context_color};
    color: {_color};
    min-height: {_height}px;   /* NEW: Set minimum height */
}}
QLineEdit:focus {{
    border: {_border_size}px solid {_context_color};
    background-color: {_bg_color_active};
}}
'''

# PY PUSH BUTTON
# ///////////////////////////////////////////////////////////////
# PY PUSH BUTTON
# ///////////////////////////////////////////////////////////////
class PyLineEdit(QLineEdit):
    def __init__(
        self, 
        text = "",
        place_holder_text = "",
        radius = 8,
        border_size = 2,
        color = "#FFF",
        selection_color = "#FFF",
        bg_color = "#333",
        bg_color_active = "#222",
        context_color = "#00ABE8",
        height = 50  # NEW: Height parameter
    ):
        super().__init__()

        # PARAMETERS
        if text:
            self.setText(text)
        if place_holder_text:
            self.setPlaceholderText(place_holder_text)

        # SET FIXED HEIGHT
        self.setFixedHeight(height)

        # SET STYLESHEET
        self.set_stylesheet(
            radius,
            border_size,
            color,
            selection_color,
            bg_color,
            bg_color_active,
            context_color,
            height  # Pass the height to the stylesheet
        )

    # SET STYLESHEET
    def set_stylesheet(
        self,
        radius,
        border_size,
        color,
        selection_color,
        bg_color,
        bg_color_active,
        context_color,
        height  # NEW: Add height to the stylesheet formatting
    ):
        # APPLY STYLESHEET
        style_format = style.format(
            _radius = radius,
            _border_size = border_size,           
            _color = color,
            _selection_color = selection_color,
            _bg_color = bg_color,
            _bg_color_active = bg_color_active,
            _context_color = context_color,
            _height = height  # NEW: Format the height into the stylesheet
        )
        self.setStyleSheet(style_format)
