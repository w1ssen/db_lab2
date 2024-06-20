import sys
import selects
import classes
import students
import prizes
import punishments
from PyQt6.QtWidgets import QPushButton, QMessageBox, QApplication, QVBoxLayout, QTableWidget, QTableWidgetItem, QWidget, QHBoxLayout
from PyQt6.QtWidgets import QLineEdit, QDialog, QLabel, QFileDialog
from PyQt6.QtCore import QByteArray
from PyQt6.QtGui import QIcon, QPixmap, QImage


class Punish_Table(QWidget):
    def __init__(self, db, cursor):
        super().__init__()
        self.db = db
        self.cursor = cursor
        self.photo = None
        self.setWindowTitle('惩罚')
        self.resize(500, 500)
        self.init_ui()

    def init_ui(self):
        info = selects.select_punish_all(self.db, self.cursor)

        leninfo = 3
        self.table = QTableWidget(len(info), leninfo)
        self.table.setHorizontalHeaderLabels(['学号', '惩罚','日期'])


        # 填充表格数据
        for i in range(len(info)):
            for j in range(leninfo):
                item = QTableWidgetItem(str(info[i][j]))
                self.table.setItem(i, j, item)


        # 添加学生信息的输入框和按钮
        self.inputLayout = QHBoxLayout()
        self.student_id_input = QLineEdit()
        self.student_id_input.setPlaceholderText('学号')
        self.student_name_input = QLineEdit()
        self.student_name_input.setPlaceholderText('惩罚')
        self.student_age_input = QLineEdit()
        self.student_age_input.setPlaceholderText('日期')

        self.add_student_button = QPushButton('添加惩罚')
        self.add_student_button.clicked.connect(self.add_student)

        self.inputLayout.addWidget(QLabel('学号:'))
        self.inputLayout.addWidget(self.student_id_input)
        self.inputLayout.addWidget(QLabel('惩罚:'))
        self.inputLayout.addWidget(self.student_name_input)
        self.inputLayout.addWidget(QLabel('日期:'))
        self.inputLayout.addWidget(self.student_age_input)
        self.inputLayout.addWidget(self.add_student_button)


        self.inputLayout1 = QHBoxLayout()
        self.student_id_input1 = QLineEdit()
        self.student_id_input1.setPlaceholderText('学号')
        self.student_name_input1 = QLineEdit()
        self.student_name_input1.setPlaceholderText('惩罚')
        self.del_student_button = QPushButton('删除奖项')
        self.del_student_button.clicked.connect(self.delete_student)


        self.inputLayout1.addWidget(QLabel('学号:'))
        self.inputLayout1.addWidget(self.student_id_input1)
        self.inputLayout1.addWidget(QLabel('惩罚:'))
        self.inputLayout1.addWidget(self.student_name_input1)
        self.inputLayout1.addWidget(self.del_student_button)



        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addLayout(self.inputLayout)
        layout.addLayout(self.inputLayout1)
        self.setLayout(layout)


    def load_data(self):

        info = selects.select_punish_all(self.db, self.cursor)
        leninfo = 3
        headers = ['学号', '惩罚','日期']

        self.table.setRowCount(len(info))
        self.table.setColumnCount(leninfo)
        self.table.setHorizontalHeaderLabels(headers)

        for i in range(len(info)):
            for j in range(leninfo):
                item = QTableWidgetItem(str(info[i][j]))
                self.table.setItem(i, j, item)

    def delete_student(self):
        student_id = self.student_id_input1.text()
        student_name = self.student_name_input1.text()
        #print(student_id)

        if not (student_id and student_name):
            QMessageBox.warning(self, '输入为空')
            return

        # 将学生信息插入数据库
        try:
            punishments.delete_punishtime(self.db, self.cursor, student_id, student_name)
            self.load_data()
            widget = QWidget()
            QMessageBox.information(widget, '信息', '删除成功')  # 触发的事件时弹出会话框
        except Exception as e:
            print(f"发生错误：{e}")
            return

    def add_student(self):
        student_id = self.student_id_input.text()
        student_name = self.student_name_input.text()
        student_age = self.student_age_input.text()
        #print(student_id)

        if not (student_id and student_name and student_age):
            QMessageBox.warning(self, '输入错误', '所有字段都是必填的。')
            return

            # 将学生信息插入数据库
        try:
            punishments.add_punishtime(self.db, self.cursor, student_id, student_name, student_age)
            self.load_data()
            widget = QWidget()
            QMessageBox.information(widget, '信息', '添加成功')  # 触发的事件时弹出会话框

        except Exception as e:
            print(f"发生错误：{e}")
            return


