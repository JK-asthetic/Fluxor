
from qt_core import *
from pathlib import Path
from gui.widgets import *

class Ui_MainPages(object):
    
    def setupUi(self, MainPages):
        if not MainPages.objectName():
            MainPages.setObjectName(u"MainPages")
        MainPages.resize(860, 600)
        self.main_pages_layout = QVBoxLayout(MainPages)
        self.main_pages_layout.setSpacing(0)
        self.main_pages_layout.setObjectName(u"main_pages_layout")
        self.main_pages_layout.setContentsMargins(5, 5, 5, 5)

        self.pages = QStackedWidget(MainPages)
        self.pages.setObjectName(u"pages")

        # Page 1 setup remains the same
        self.page_1 = QWidget()
        self.page_1.setObjectName(u"page_1")
        self.page_1.setStyleSheet(u"font-size: 14pt")
        self.page_1_layout = QVBoxLayout(self.page_1)
        self.page_1_layout.setSpacing(5)
        self.page_1_layout.setObjectName(u"page_1_layout")
        self.page_1_layout.setContentsMargins(5, 5, 5, 5)

        self.welcome_base = QFrame(self.page_1)
        self.welcome_base.setObjectName(u"welcome_base")
        self.welcome_base.setMinimumSize(QSize(300, 150))
        self.welcome_base.setMaximumSize(QSize(300, 150))
        self.welcome_base.setFrameShape(QFrame.NoFrame)
        self.welcome_base.setFrameShadow(QFrame.Raised)

        self.center_page_layout = QVBoxLayout(self.welcome_base)
        self.center_page_layout.setSpacing(10)
        self.center_page_layout.setObjectName(u"center_page_layout")
        self.center_page_layout.setContentsMargins(0, 0, 0, 0)

        self.logo = QFrame(self.welcome_base)
        self.logo.setObjectName(u"logo")
        self.logo.setMinimumSize(QSize(300, 120))
        self.logo.setMaximumSize(QSize(300, 120))
        self.logo.setFrameShape(QFrame.NoFrame)
        self.logo.setFrameShadow(QFrame.Raised)
        self.logo_layout = QVBoxLayout(self.logo)
        self.logo_layout.setSpacing(0)
        self.logo_layout.setObjectName(u"logo_layout")
        self.logo_layout.setContentsMargins(0, 0, 0, 0)

        self.center_page_layout.addWidget(self.logo)
        self.label = QLabel(self.welcome_base)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.center_page_layout.addWidget(self.label)


        self.page_1_layout.addWidget(self.welcome_base, 0, Qt.AlignHCenter)

        self.pages.addWidget(self.page_1)
        # ... (rest of page 1 setup)

        # Page 2 setup remains the same
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.page_2_layout = QVBoxLayout(self.page_2)
        self.page_2_layout.setSpacing(5)
        self.page_2_layout.setObjectName(u"page_2_layout")
        self.page_2_layout.setContentsMargins(5, 5, 5, 5)

        self.scroll_area = QScrollArea(self.page_2)
        self.scroll_area.setObjectName(u"scroll_area")
        self.scroll_area.setStyleSheet(u"background: transparent;")
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)

        self.contents = QWidget()
        self.contents.setObjectName(u"contents")
        self.contents.setGeometry(QRect(0, 0, 840, 580))
        self.contents.setStyleSheet(u"background: transparent;")

        self.verticalLayout = QVBoxLayout(self.contents)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)

        self.title_label = QLabel(self.contents)
        self.title_label.setObjectName(u"title_label")
        self.title_label.setMaximumSize(QSize(16777215, 40))
        
        font = QFont()
        font.setPointSize(16)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet(u"font-size: 16pt")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.title_label)

        self.description_label = QLabel(self.contents)
        self.description_label.setObjectName(u"description_label")
        self.description_label.setAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.description_label.setWordWrap(True)

        self.verticalLayout.addWidget(self.description_label)

        self.row_1_layout = QHBoxLayout()
        self.row_1_layout.setObjectName(u"row_1_layout")

        self.verticalLayout.addLayout(self.row_1_layout)

        self.row_2_layout = QHBoxLayout()
        self.row_2_layout.setObjectName(u"row_2_layout")

        self.verticalLayout.addLayout(self.row_2_layout)

        self.row_3_layout = QHBoxLayout()
        self.row_3_layout.setObjectName(u"row_3_layout")

        self.verticalLayout.addLayout(self.row_3_layout)

        self.row_4_layout = QVBoxLayout()
        self.row_4_layout.setObjectName(u"row_4_layout")

        self.verticalLayout.addLayout(self.row_4_layout)

        self.row_5_layout = QVBoxLayout()
        self.row_5_layout.setObjectName(u"row_5_layout")

        self.verticalLayout.addLayout(self.row_5_layout)

        self.scroll_area.setWidget(self.contents)

        self.page_2_layout.addWidget(self.scroll_area)

        self.pages.addWidget(self.page_2)
        # ... (rest of page 2 setup)

        # Updated Page 3 setup
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.page_3.setStyleSheet(u"QFrame {\n"
"	font-size: 16pt;\n"
"}")
        self.page_3_layout = QVBoxLayout(self.page_3)
        self.page_3_layout.setObjectName(u"page_3_layout")
        self.page_3_layout.setContentsMargins(5, 5, 5, 5)

        self.scroll_area_3 = QScrollArea(self.page_3)
        self.scroll_area_3.setObjectName(u"scroll_area_3")
        self.scroll_area_3.setStyleSheet(u"background: transparent;")
        self.scroll_area_3.setFrameShape(QFrame.NoFrame)
        self.scroll_area_3.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area_3.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area_3.setWidgetResizable(True)

        self.contents_3 = QWidget()
        self.contents_3.setObjectName(u"contents_3")
        self.contents_3.setGeometry(QRect(0, 0, 840, 580))
        self.contents_3.setStyleSheet(u"background: transparent;")

        self.verticalLayout_3 = QVBoxLayout(self.contents_3)
        self.verticalLayout_3.setSpacing(15)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(5, 5, 5, 5)

        self.title_label_3 = QLabel(self.contents_3)
        self.title_label_3.setObjectName(u"title_label_3")
        self.title_label_3.setMaximumSize(QSize(16777215, 40))
        
        font = QFont()
        font.setPointSize(16)
        self.title_label_3.setFont(font)
        self.title_label_3.setStyleSheet(u"font-size: 16pt")
        self.title_label_3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.title_label_3)


        self.row_1_layout_3 = QHBoxLayout()
        self.row_1_layout_3.setObjectName(u"row_1_layout_3")

        self.verticalLayout_3.addLayout(self.row_1_layout_3)

        self.row_2_layout_3 = QHBoxLayout()
        self.row_2_layout_3.setObjectName(u"row_2_layout_3")

        self.verticalLayout_3.addLayout(self.row_2_layout_3)

        self.row_3_layout_3 = QHBoxLayout()
        self.row_3_layout_3.setObjectName(u"row_3_layout_3")

        self.verticalLayout_3.addLayout(self.row_3_layout_3)

        self.row_4_layout_3 = QVBoxLayout()
        self.row_4_layout_3.setObjectName(u"row_4_layout_3")

        self.verticalLayout_3.addLayout(self.row_4_layout_3)

        self.row_5_layout_3 = QVBoxLayout()
        self.row_5_layout_3.setObjectName(u"row_5_layout_3")

        self.verticalLayout_3.addLayout(self.row_5_layout_3)

        self.scroll_area_3.setWidget(self.contents_3)

        self.page_3_layout.addWidget(self.scroll_area_3)

        self.pages.addWidget(self.page_3)
        

        # Page 4 setup
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.page_4_layout = QVBoxLayout(self.page_4)
        self.page_4_layout.setObjectName(u"page_4_layout")
        self.page_4_layout.setContentsMargins(5, 5, 5, 5)

        self.scroll_area_4 = QScrollArea(self.page_4)
        self.scroll_area_4.setObjectName(u"scroll_area_4")
        self.scroll_area_4.setStyleSheet(u"background: transparent;")
        self.scroll_area_4.setFrameShape(QFrame.NoFrame)
        self.scroll_area_4.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area_4.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area_4.setWidgetResizable(True)

        self.contents_4 = QWidget()
        self.contents_4.setObjectName(u"contents_4")
        self.contents_4.setGeometry(QRect(0, 0, 840, 580))
        self.contents_4.setStyleSheet(u"background: transparent;")

        self.verticalLayout_4 = QVBoxLayout(self.contents_4)
        self.verticalLayout_4.setSpacing(15)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(5, 5, 5, 5)

        self.title_label_4 = QLabel(self.contents_4)
        self.title_label_4.setObjectName(u"title_label_4")
        self.title_label_4.setMaximumSize(QSize(16777215, 40))

        font = QFont()
        font.setPointSize(16)
        self.title_label_4.setFont(font)
        self.title_label_4.setStyleSheet(u"font-size: 16pt")
        self.title_label_4.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.title_label_4)

        self.row_1_layout_4 = QHBoxLayout()
        self.row_1_layout_4.setObjectName(u"row_1_layout_4")

        self.verticalLayout_4.addLayout(self.row_1_layout_4)

        self.row_2_layout_4 = QHBoxLayout()
        self.row_2_layout_4.setObjectName(u"row_2_layout_4")

        self.verticalLayout_4.addLayout(self.row_2_layout_4)

        self.row_3_layout_4 = QHBoxLayout()
        self.row_3_layout_4.setObjectName(u"row_3_layout_4")

        self.verticalLayout_4.addLayout(self.row_3_layout_4)

        self.row_4_layout_4 = QVBoxLayout()
        self.row_4_layout_4.setObjectName(u"row_4_layout_4")

        self.verticalLayout_4.addLayout(self.row_4_layout_4)

        self.row_5_layout_4 = QVBoxLayout()
        self.row_5_layout_4.setObjectName(u"row_5_layout_4")

        self.verticalLayout_4.addLayout(self.row_5_layout_4)

        self.scroll_area_4.setWidget(self.contents_4)

        self.page_4_layout.addWidget(self.scroll_area_4)

        self.pages.addWidget(self.page_4)



        # Page 5 setup for chatbot
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.page_5_layout = QVBoxLayout(self.page_5)
        self.page_5_layout.setObjectName(u"page_5_layout")
        self.page_5_layout.setContentsMargins(5, 5, 5, 5)

        # Directory Selection Area
        self.select_dir_layout = QHBoxLayout()
        self.select_dir_layout.setObjectName(u"select_dir_layout")

        # Directory Select Button
        self.select_dir_button = PyPushButton(
            text="Select the directory",
            radius=8,
            color= "#000000",
            bg_color="#dcdcdc",
            bg_color_hover="#ffffff",
            bg_color_pressed="#f0f0f0"
        )
        self.select_dir_button.setObjectName(u"select_dir_button")
        self.select_dir_button.setMinimumHeight(40)
        self.select_dir_layout.addWidget(self.select_dir_button)

        # Selected Directory Label
        self.selected_dir_label = QLabel("No directory selected")
        self.selected_dir_label.setObjectName(u"selected_dir_label")
        self.select_dir_layout.addWidget(self.selected_dir_label)

        self.page_5_layout.addLayout(self.select_dir_layout)

        # Scroll Area for Chat Messages
        self.chat_scroll_area = QScrollArea(self.page_5)
        self.chat_scroll_area.setObjectName(u"chat_scroll_area")
        self.chat_scroll_area.setStyleSheet(u"background: #f5f5f5;")
        self.chat_scroll_area.setWidgetResizable(True)

        self.chat_content = QWidget()
        self.chat_content.setObjectName(u"chat_content")
        self.chat_layout = QVBoxLayout(self.chat_content)
        self.chat_layout.setObjectName(u"chat_layout")
        self.chat_layout.setAlignment(Qt.AlignTop)

        self.chat_scroll_area.setWidget(self.chat_content)
        self.page_5_layout.addWidget(self.chat_scroll_area)

        # User Input and Send Button
        self.user_input_layout = QHBoxLayout()
        self.user_input_layout.setObjectName(u"user_input_layout")

        # Text Box for User Input
        self.user_text_input = QLineEdit()
        self.user_text_input.setObjectName("user_text_input")
        self.user_text_input.setPlaceholderText("Type your message here...")
        self.user_text_input.setMinimumHeight(40)

        # Apply the custom stylesheet
        self.user_text_input.setStyleSheet("""
            QLineEdit {
                color: #000000; /* Text color */
                background-color: #dcdcdc; /* Background color */
                border-radius: 8px; /* Rounded corners */
                padding: 5px; /* Inner padding for text */
            }
            QLineEdit:focus {
                background-color: #f0f0f0; /* Background color when focused */
            }
        """)

        self.user_input_layout.addWidget(self.user_text_input)


        # Send Button
        self.send_button = QPushButton("Send")
        self.send_button.setObjectName("send_button")
        self.send_button.setMinimumHeight(40)

        # Apply the custom stylesheet
        self.send_button.setStyleSheet("""
            QPushButton {
                color: #000000; /* Text color */
                background-color: #dcdcdc; /* Default background color */
                border-radius: 8px; /* Rounded corners */
                padding: 10px; /* Inner padding */
            }
            QPushButton:pressed {
                background-color: #f0f0f0; /* Background color when pressed */
            }
            QPushButton:hover {
                background-color: #e8e8e8; /* Background color when hovered */
            }
        """)

        self.user_input_layout.addWidget(self.send_button)
        self.page_5_layout.addLayout(self.user_input_layout)

        # Add page_5 to stacked widget
        self.pages.addWidget(self.page_5)



#  --------------------
        self.main_pages_layout.addWidget(self.pages)

        self.retranslateUi(MainPages)

        self.pages.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(MainPages)

    def retranslateUi(self, MainPages):
        MainPages.setWindowTitle(QCoreApplication.translate("MainPages", u"Form", None))
        self.label.setText(QCoreApplication.translate("MainPages", u"Welcome To Fluxor", None))
        self.title_label.setText(QCoreApplication.translate("MainPages", u"File Classifier", None))
        self.description_label.setText(QCoreApplication.translate("MainPages", u"Here user could re-arrange their Directories via selecting directory through Button below.\n"
"We have tried to implement feature like user Preference for better User Experience by having imput formt he user on how they would like to clasify their directries", None))
        self.title_label_3.setText(QCoreApplication.translate("MainPages", u"Re-name file with AI", None))
        self.title_label_4.setText(QCoreApplication.translate("MainPages", u"Classify Your file Based on Type", None))
        # self.title_label_5.setText(QCoreApplication.translate("MainPages", u"Summarize Yor File With AI", None))