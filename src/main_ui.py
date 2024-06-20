import sys
import selects
import classes
import students
import stu_table
import class_table
import prize_table
import punish_table
import search_stu
import score_table
import prizes
import punishments
from PyQt6.QtWidgets import QPushButton, QMessageBox, QApplication, QVBoxLayout, QTableWidget, QTableWidgetItem, QWidget, QHBoxLayout
from PyQt6.QtWidgets import QLineEdit, QDialog, QLabel, QFileDialog
from PyQt6.QtCore import QByteArray
from PyQt6.QtGui import QIcon, QPixmap, QImage

class Main_Window(QWidget):
    def __init__(self, db, cursor):
        super().__init__()
        self.db = db
        self.cursor = cursor
        self.setWindowTitle('学籍管理系统 管理员界面')
        self.resize(600, 400)
        self.setWindowIcon(QIcon('./picture/logo.png'))
        self.btn1 = QPushButton('查看全部学生', self)
        self.btn2 = QPushButton('查看全部课程', self)
        self.btn3 = QPushButton('查看全部奖项', self)
        self.btn4 = QPushButton('查看全部惩罚', self)
        self.btn5 = QPushButton('查看成绩信息', self)
        self.btn6 = QPushButton('查询学生信息', self)
        self.init_ui()

    def init_ui(self):
        self.btn1.resize(200, 200)
        self.btn1.move(0, 0)  # 按钮的位置
        self.btn1.clicked.connect(self.check_all_students)

        self.btn2.resize(200, 200)
        self.btn2.move(0, 200)  # 按钮的位置
        self.btn2.clicked.connect(self.check_all_classes)

        self.btn3.resize(200, 200)
        self.btn3.move(200, 0)  # 按钮的位置
        self.btn3.clicked.connect(self.check_all_prizes)

        self.btn4.resize(200, 200)
        self.btn4.move(200, 200)  # 按钮的位置
        self.btn4.clicked.connect(self.check_all_punish)

        self.btn5.resize(200, 200)
        self.btn5.move(400, 0)  # 按钮的位置
        self.btn5.clicked.connect(self.check_all_score)

        self.btn6.resize(200, 200)
        self.btn6.move(400, 200)  # 按钮的位置
        self.btn6.clicked.connect(self.search_stu)

    def check_all_students(self):
        self.tableWindow = stu_table.Stu_Table(self.db, self.cursor)
        self.tableWindow.show()

    def check_all_classes(self):
        self.tableWindow = class_table.Class_Table(self.db, self.cursor)
        self.tableWindow.show()

    def check_all_prizes(self):
        self.tableWindow = prize_table.Prize_Table(self.db, self.cursor)
        self.tableWindow.show()

    def check_all_punish(self):
        self.tableWindow = punish_table.Punish_Table(self.db, self.cursor)
        self.tableWindow.show()

    def check_all_score(self):
            self.tableWindow = score_table.Score_Table(self.db, self.cursor)
            self.tableWindow.show()

    def search_stu(self):
        self.tableWindow = search_stu.Search_Stu(self.db, self.cursor)
        self.tableWindow.show()

