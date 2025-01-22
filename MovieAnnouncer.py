from PyQt6 import QtWidgets, QtGui, QtCore
import sys
import requests

class MovieBotApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Discord Movie Bot")
        self.setGeometry(100, 100, 600, 500)

        # Set main window background color
        self.setStyleSheet("background-color: #070e12;")

        layout = QtWidgets.QVBoxLayout()

        # Add Title
        title_label = QtWidgets.QLabel("YourIPTVDealer Movie BOT")
        title_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold; margin-bottom: 20px;")
        title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Add dropdown to switch between Movie and Series
        type_layout = QtWidgets.QHBoxLayout()
        type_label = QtWidgets.QLabel("Select Type:")
        type_label.setStyleSheet("color: white;")
        self.type_selector = QtWidgets.QComboBox()
        self.type_selector.addItems(["Movie", "Series"])
        self.type_selector.setStyleSheet("background-color: #0c1a20; color: white; border-radius: 5px; padding: 5px;")
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.type_selector)
        layout.addLayout(type_layout)

        # Add padding around the fields
        form_layout = QtWidgets.QFormLayout()
        form_layout.setHorizontalSpacing(20)
        form_layout.setVerticalSpacing(15)

        # Styled Movie Name input
        movie_name_label = QtWidgets.QLabel("Name:")
        movie_name_label.setStyleSheet("color: white;")
        self.movie_name = QtWidgets.QLineEdit()
        self.movie_name.setStyleSheet("background-color: #0c1a20; color: white; border: 1px solid #1e2a30; padding: 5px; border-radius: 5px;")
        form_layout.addRow(movie_name_label, self.movie_name)

        # Styled Country input
        country_label = QtWidgets.QLabel("Country (Shortcode):")
        country_label.setStyleSheet("color: white;")
        self.country_code = QtWidgets.QLineEdit()
        self.country_code.setStyleSheet("background-color: #0c1a20; color: white; border: 1px solid #1e2a30; padding: 5px; border-radius: 5px;")
        form_layout.addRow(country_label, self.country_code)

        # Styled Subs input
        subs_label = QtWidgets.QLabel("Subs:")
        subs_label.setStyleSheet("color: white;")
        self.subs = QtWidgets.QLineEdit()
        self.subs.setStyleSheet("background-color: #0c1a20; color: white; border: 1px solid #1e2a30; padding: 5px; border-radius: 5px;")
        form_layout.addRow(subs_label, self.subs)

        # Additional Movies/Series
        additional_label = QtWidgets.QLabel("Additional Movies/Series Added:")
        additional_label.setStyleSheet("color: white;")
        self.additional_area = QtWidgets.QTextEdit()
        self.additional_area.setStyleSheet("background-color: #0c1a20; color: white; border: 1px solid #1e2a30; padding: 5px; border-radius: 5px;")
        form_layout.addRow(additional_label, self.additional_area)

        # Styled Main Image URL
        main_image_label = QtWidgets.QLabel("Main Image URL (bottom):")
        main_image_label.setStyleSheet("color: white;")
        self.main_image_url = QtWidgets.QLineEdit()
        self.main_image_url.setStyleSheet("background-color: #0c1a20; color: white; border: 1px solid #1e2a30; padding: 5px; border-radius: 5px;")
        form_layout.addRow(main_image_label, self.main_image_url)

        layout.addLayout(form_layout)

        # Styled Submit button
        self.submit_button = QtWidgets.QPushButton("Send to Discord")
        self.submit_button.setStyleSheet(
            "background-color: #1e2a30; color: white; border: 1px solid #1e2a30; padding: 10px; margin-top: 20px; border-radius: 5px; cursor: pointer;"
        )
        self.submit_button.clicked.connect(self.send_to_discord)
        layout.addWidget(self.submit_button, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(layout)

    def send_to_discord(self):
        # Hardcoded values for removed fields
        webhook_url = "https://discord.com/api/webhooks/1331748717895876660/CX3fiGM_paaS22F4dYgE2ei1vYwLXsSzPpQrCWAAIfx8VWksMGUQDZdmDpNetR6OQXtd"
        author_image_url = "https://i.ibb.co/JjY6SNh/cropped-favicon-2.png"

        type_selected = self.type_selector.currentText()
        title = f"New {type_selected} Added!"

        additional_content = self.additional_area.toPlainText().strip()
        additional_field = {"name": f"Additional {type_selected}(s)", "value": additional_content, "inline": False} if additional_content else None

        fields = [
            {"name": "Name", "value": self.movie_name.text(), "inline": False},
            {"name": "Country", "value": self.country_code.text(), "inline": True},
            {"name": "Subs", "value": self.subs.text(), "inline": True},
            {"name": "Website", "value": "https://youriptvdealer.com", "inline": False}
        ]

        if additional_field:
            fields.append(additional_field)

        data = {
            "embeds": [
                {
                    "title": title,
                    "fields": fields,
                    "thumbnail": {"url": author_image_url},
                    "image": {"url": self.main_image_url.text()}
                }
            ]
        }

        response = requests.post(webhook_url, json=data)
        if response.status_code == 204:
            QtWidgets.QMessageBox.information(self, "Success", f"{type_selected} announcement sent successfully!")
        else:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to send announcement. Status Code: {response.status_code}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MovieBotApp()
    window.show()
    sys.exit(app.exec())
