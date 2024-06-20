import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
import pymysql
import search_stu
import sys
import main_ui
import change_password
import init
import punishments
from PyQt6.QtWidgets import QPushButton, QMessageBox, QApplication, QVBoxLayout, QTableWidget, QTableWidgetItem, \
    QWidget, QHBoxLayout
from PyQt6.QtWidgets import QLineEdit, QDialog, QLabel, QFileDialog
from PyQt6.QtCore import QByteArray
from PyQt6.QtGui import QIcon, QPixmap, QImage


def open_main_window(self):
    db = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="lab2"
    )
    cursor = db.cursor()
    # init.init(db, cursor)
    self.main_window = main_ui.Main_Window(db, cursor)
    self.main_window.show()



def open_user_window(self):
    db = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="lab2"
    )
    cursor = db.cursor()
    self.main_window = search_stu.ResultWindow(db, cursor, self.user_input.text())
    self.main_window.show()



def authenticate_admin(self, username, password):
    try:
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="lab2"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
        result = cursor.fetchone()
        connection.close()

        if result:
            return True
        else:
            return False
    except pymysql.connect.Error as err:
        QMessageBox.critical(self, "错误", f"数据库连接失败: {err}")
        return False


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
        QMessageBox.critical(self, "错误", f"数据库连接失败: {err}")
        return False
