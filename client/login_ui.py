import sys
import requests
from PyQt5.QtWidgets import (QApplication,QWidget,QVBoxLayout,QLineEdit,QPushButton,QMessageBox,QLabel)
from PyQt5.QtGui import QColor , QFont , QPalette


SERVER_URL = "http://127.0.0.1:8000"

class AdvancedAuthSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.resize(400,300)

        layout = QVBoxLayout(self)

        palette = QPalette()
        palette.setColor(QPalette.Window,QColor("#F6F0D7"))
        self.setPalette(palette)

        self.username_entry = QLineEdit()
        self.username_entry.setPlaceholderText("username...")
        self.username_entry.setFont(QFont("San Francisco",14))
        layout.addWidget(self.username_entry)

        self.password_entry = QLineEdit()
        self.password_entry.setPlaceholderText("Password...")
        self.password_entry.setFont(QFont("San Francisco",14))
        self.password_entry.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_entry)

        self.login_btn = QPushButton("login")
        self.login_btn.setFont(QFont("San Francisco",14))
        self.login_btn.clicked.connect(self.login)
        layout.addWidget(self.login_btn)

        self.register_btn = QPushButton("register")
        self.register_btn.clicked.connect(self.register)
        self.register_btn.setFont(QFont("San Francisco",14))
        layout.addWidget(self.register_btn)

    
    def register(self):
        username = self.username_entry.text()
        password = self.password_entry.text()

        data = {
            "username":username,
            "password":password
        }

        r = requests.post(f"{SERVER_URL}/register",json=data)
        res = r.json()

        if "error" in res:
            QMessageBox.warning(self,"register info",res["error"])
        else:
            QMessageBox.information(self,"success",res["message"])


    

    def login(self):
        username = self.username_entry.text()
        password = self.password_entry.text()

        data = {
            "username":username,
            "password":password
        }

        r = requests.post(f"{SERVER_URL}/login",json=data)
        res = r.json()

        if "error" in res:
            QMessageBox.warning(self,"register info",res["error"])
        else:
            QMessageBox.information(self,"success","welcome")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = AdvancedAuthSystem()
    w.show()
    sys.exit(app.exec_())
