import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
import pymysql
import search_stu
import sys
import main_ui
import change_password
import authenticate
import init
import punishments
from PyQt6.QtWidgets import QPushButton, QMessageBox, QApplication, QVBoxLayout, QTableWidget, QTableWidgetItem, \
    QWidget, QHBoxLayout
from PyQt6.QtWidgets import QLineEdit, QDialog, QLabel, QFileDialog
from PyQt6.QtCore import QByteArray
from PyQt6.QtGui import QIcon, QPixmap, QImage


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("学籍管理系统 登录")
        self.setGeometry(600, 300, 300, 200)

        self.layout = QVBoxLayout()

        self.user_label = QLabel("用户名:")
        self.layout.addWidget(self.user_label)
        self.user_input = QLineEdit()
        self.layout.addWidget(self.user_input)

        self.password_label = QLabel("密码:")
        self.layout.addWidget(self.password_label)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.password_input)

        self.login_button = QPushButton("登录")
        self.login_button.clicked.connect(self.check_login)
        self.layout.addWidget(self.login_button)

        self.change_button = QPushButton("修改密码")
        self.change_button.clicked.connect(self.change_password)
        self.layout.addWidget(self.change_button)

        self.setLayout(self.layout)


    def change_password(self):
        self.Window = change_password.Change_Password_Window()
        self.Window.show()
        self.close()

    def check_login(self):
        username = self.user_input.text()
        password = self.password_input.text()

        if authenticate.authenticate_admin(self, username, password):
            authenticate.open_main_window(self)
        elif authenticate.authenticate_user(self, username, password):
            authenticate.open_user_window(self)
        else:
            QMessageBox.warning(self, "失败", "用户名或密码错误!")

