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

        self.token = None

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

        self.dashboard_btn = QPushButton("Open Dashboard")
        self.dashboard_btn.clicked.connect(self.open_dashboard)
        self.dashboard_btn.setFont(QFont("San Francisco",14))
        self.dashboard_btn.setEnabled(False)
        layout.addWidget(self.dashboard_btn)

    
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
        try:
            if "token" in res:
                self.token = res["token"]
                QMessageBox.information(self,"success","Login successful")
                self.dashboard_btn.setEnabled(True)
            else:
                QMessageBox.warning(self,"error","Login failed")
        except Exception as e:
            QMessageBox.critical(self,"Network Error",str(e))
    
    def open_dashboard(self):
        headers = {
            "Authorization":self.token
        }

        try:
            r = requests.get(f"{SERVER_URL}/protected",headers=headers)
            res = r.json()

            if "message" in res:
                QMessageBox.information(self,"Dashboard",res["message"])
            else:
                QMessageBox.warning(self,"Error",res.get("error","Access denied"))
        except Exception as e:
            QMessageBox.critical(self,"Network Error",str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = AdvancedAuthSystem()
    w.show()
    sys.exit(app.exec_())
