from PyQt6 import QtWidgets, QtGui, QtCore
import sys
import requests
from dotenv import load_dotenv
import os

# Check the .env file to configure it the way you want. I have set an example usage, but you can customize it completely
load_dotenv()

class MovieBotApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(os.getenv("UI_TITLE"))
        self.setGeometry(100, 100, 600, 500)
        self.setStyleSheet("background-color: #070e12;")
        layout = QtWidgets.QVBoxLayout()

        # Title
        self.title_label = QtWidgets.QLabel(os.getenv("UI_TITLE"))
        self.title_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold; margin-bottom: 20px;")
        self.title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)

        
        form_layout = QtWidgets.QFormLayout()
        form_layout.setHorizontalSpacing(20)
        form_layout.setVerticalSpacing(15)

        #  FIELD1 
        self.field1_label = QtWidgets.QLabel(os.getenv("FIELD1_TITLE"))
        self.field1_label.setStyleSheet("color: white;")
        self.field1_input = QtWidgets.QLineEdit()
        self.field1_input.setStyleSheet("background-color: #0c1a20; color: white; border: 1px solid #1e2a30; padding: 5px; border-radius: 5px;")
        form_layout.addRow(self.field1_label, self.field1_input)

        #  INLINE1 
        self.inline1_label = QtWidgets.QLabel(os.getenv("INLINE1_TITLE"))
        self.inline1_label.setStyleSheet("color: white;")
        self.inline1_input = QtWidgets.QLineEdit()
        self.inline1_input.setStyleSheet("background-color: #0c1a20; color: white; border: 1px solid #1e2a30; padding: 5px; border-radius: 5px;")
        form_layout.addRow(self.inline1_label, self.inline1_input)

        #  INLINE2 
        self.inline2_label = QtWidgets.QLabel(os.getenv("INLINE2_TITLE"))
        self.inline2_label.setStyleSheet("color: white;")
        self.inline2_input = QtWidgets.QLineEdit()
        self.inline2_input.setStyleSheet("background-color: #0c1a20; color: white; border: 1px solid #1e2a30; padding: 5px; border-radius: 5px;")
        form_layout.addRow(self.inline2_label, self.inline2_input)

        #  FIELD4 
        self.field4_label = QtWidgets.QLabel(os.getenv("FIELD4_TITLE"))
        self.field4_label.setStyleSheet("color: white;")
        self.field4_input = QtWidgets.QTextEdit()
        self.field4_input.setStyleSheet("background-color: #0c1a20; color: white; border: 1px solid #1e2a30; padding: 5px; border-radius: 5px;")
        form_layout.addRow(self.field4_label, self.field4_input)

        #  FIELD3 
        self.field3_label = QtWidgets.QLabel(os.getenv("FIELD3_TITLE"))
        self.field3_label.setStyleSheet("color: white;")
        self.field3_input = QtWidgets.QLineEdit()
        self.field3_input.setStyleSheet("background-color: #0c1a20; color: white; border: 1px solid #1e2a30; padding: 5px; border-radius: 5px;")
        form_layout.addRow(self.field3_label, self.field3_input)

        # IMG 
        self.main_image_label = QtWidgets.QLabel("Main Image URL")
        self.main_image_label.setStyleSheet("color: white;")
        self.main_image_input = QtWidgets.QLineEdit()
        self.main_image_input.setStyleSheet("background-color: #0c1a20; color: white; border: 1px solid #1e2a30; padding: 5px; border-radius: 5px;")
        form_layout.addRow(self.main_image_label, self.main_image_input)

        layout.addLayout(form_layout)

        
        self.submit_button = QtWidgets.QPushButton("Send to Discord")
        self.submit_button.setStyleSheet(
            "background-color: #1e2a30; color: white; border: 1px solid #1e2a30; padding: 10px; margin-top: 20px; border-radius: 5px; cursor: pointer;"
        )
        self.submit_button.clicked.connect(self.send_to_discord)
        layout.addWidget(self.submit_button, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(layout)

    def send_to_discord(self):
        webhook_url = os.getenv("WEBHOOK_URL")

        title = os.getenv("TITLE1")

        additional_content = self.field4_input.toPlainText().strip()
        additional_field = {"name": os.getenv("FIELD4_TITLE"), "value": additional_content, "inline": False} if additional_content else None

        fields = [
            {"name": os.getenv("FIELD1_TITLE"), "value": self.field1_input.text(), "inline": False},
            {"name": os.getenv("INLINE1_TITLE"), "value": self.inline1_input.text(), "inline": True},
            {"name": os.getenv("INLINE2_TITLE"), "value": self.inline2_input.text(), "inline": True},
            {"name": os.getenv("FIELD3_TITLE"), "value": self.field3_input.text(), "inline": False}
        ]

        if additional_field:
            fields.append(additional_field)

        data = {
            "embeds": [
                {
                    "title": title,
                    "color": 0x10d0e6,
                    "fields": fields,
                    "thumbnail": {"url": os.getenv("AUTHOR_IMAGE_URL")},
                    "image": {"url": self.main_image_input.text()}
                }
            ]
        }

        response = requests.post(webhook_url, json=data)
        if response.status_code == 204:
            QtWidgets.QMessageBox.information(self, "Success", "Announcement sent successfully!")
        else:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to send announcement. Status Code: {response.status_code}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MovieBotApp()
    window.show()
    sys.exit(app.exec())
