import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
import pymysql
import login
import search_stu
import sys
import main_ui
import punishments
from PyQt6.QtWidgets import QPushButton, QMessageBox, QApplication, QVBoxLayout, QTableWidget, QTableWidgetItem, \
    QWidget, QHBoxLayout
from PyQt6.QtWidgets import QLineEdit, QDialog, QLabel, QFileDialog
from PyQt6.QtCore import QByteArray
from PyQt6.QtGui import QIcon, QPixmap, QImage


class Change_Password_Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("修改密码")
        self.setGeometry(600, 300, 300, 200)

        self.layout = QVBoxLayout()

        self.user_label = QLabel("用户名:")
        self.layout.addWidget(self.user_label)
        self.user_input = QLineEdit()
        self.layout.addWidget(self.user_input)

        self.password_label = QLabel("原密码:")
        self.layout.addWidget(self.password_label)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.password_input)

        self.password_label1 = QLabel("新密码:")
        self.layout.addWidget(self.password_label1)
        self.password_input1 = QLineEdit()
        self.password_input1.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.password_input1)

        self.login_button = QPushButton("修改密码")
        self.login_button.clicked.connect(self.check_login)
        self.layout.addWidget(self.login_button)

        self.setLayout(self.layout)


    def check_login(self):
        username = self.user_input.text()
        password = self.password_input.text()
        new_password = self.password_input1.text()

        if self.authenticate_user(username, password):
            if self.change_password(username, new_password):
                QMessageBox.information(self,"成功", "修改成功!")
                self.Window = login.LoginWindow()
                self.Window.show()
                self.close()
        else:
            QMessageBox.warning(self, "失败", "用户名或密码错误!")


    def authenticate_user(self, username, password):
        try:
            connection = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                database="lab2"
            )
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
            result = cursor.fetchone()
            connection.close()

            if result:
                return True
            else:
                return False
        except pymysql.connect.Error as err:
            QMessageBox.critical(self, "错误0", f"数据库连接失败: {err}")
            return False

    def change_password(self, username, password):
                db = pymysql.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="lab2"
                )
                cursor = db.cursor()

                #def add_class(db, cursor, ID, name, point):
                sql = "UPDATE users SET password = %s WHERE username = %s"
                try:
                    cursor.execute(sql, (password, username))
                    db.commit()
                    return True
                except Exception as e:
                    print(f"发生错误：{e}")
                    db.rollback()
                    return False
