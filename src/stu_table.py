
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


class Stu_Table(QWidget):
    def __init__(self, db, cursor):
        super().__init__()
        self.db = db
        self.cursor = cursor
        self.photo = None
        self.setWindowTitle('学生名单')
        self.resize(500, 500)
        self.init_ui()

    def init_ui(self):
        info = selects.select_students_all(self.db, self.cursor)
        leninfo = 4
        self.table = QTableWidget(len(info), leninfo)
        self.table.setHorizontalHeaderLabels(['学号', '姓名', '年龄', '专业'])

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
        self.student_name_input.setPlaceholderText('姓名')
        self.student_age_input = QLineEdit()
        self.student_age_input.setPlaceholderText('年龄')
        self.student_major_input = QLineEdit()
        self.student_major_input.setPlaceholderText('专业')
        # 创建上传照片按钮
        self.chooseButton = QPushButton('选择要上传的照片', self)
        self.chooseButton.clicked.connect(self.choosePhoto)
        self.add_student_button = QPushButton('添加学生')
        self.add_student_button.clicked.connect(self.add_student)

        self.inputLayout.addWidget(QLabel('学号:'))
        self.inputLayout.addWidget(self.student_id_input)
        self.inputLayout.addWidget(QLabel('姓名:'))
        self.inputLayout.addWidget(self.student_name_input)
        self.inputLayout.addWidget(QLabel('年龄:'))
        self.inputLayout.addWidget(self.student_age_input)
        self.inputLayout.addWidget(QLabel('专业:'))
        self.inputLayout.addWidget(self.student_major_input)
        self.inputLayout.addWidget(self.chooseButton)
        self.inputLayout.addWidget(self.add_student_button)


        self.inputLayout1 = QHBoxLayout()
        self.student_id_input1 = QLineEdit()
        self.student_id_input1.setPlaceholderText('学号')
        self.del_student_button = QPushButton('删除学生')
        self.del_student_button.clicked.connect(self.delete_student)
        self.change_student_Button = QPushButton('修改学生信息', self)
        self.change_student_Button.clicked.connect(self.change_student)


        self.inputLayout1.addWidget(QLabel('学号:'))
        self.inputLayout1.addWidget(self.student_id_input1)
        self.inputLayout1.addWidget(self.del_student_button)
        self.inputLayout1.addWidget(self.change_student_Button)


        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addLayout(self.inputLayout)
        layout.addLayout(self.inputLayout1)
        self.setLayout(layout)

    def choosePhoto(self):
        photo_path, _ = QFileDialog.getOpenFileName(self, "Select Photo", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if photo_path:
            # 读取图片并保存为二进制
            picture = open(photo_path, 'rb')
            pictureByte = picture.read()
            picture.close()
            self.photo = pictureByte
            self.acceptflag = True

    def load_data(self):
        info = selects.select_students_all(self.db, self.cursor)
        leninfo = 4
        headers = ['学号', '姓名', '年龄', '专业']

        self.table.setRowCount(len(info))
        self.table.setColumnCount(leninfo)
        self.table.setHorizontalHeaderLabels(headers)

        for i in range(len(info)):
            for j in range(leninfo):
                item = QTableWidgetItem(str(info[i][j]))
                self.table.setItem(i, j, item)

    def delete_student(self):
        student_id = self.student_id_input1.text()
        #print(student_id)

        if not (student_id):
            QMessageBox.warning(self, '输入为空')
            return

        # 将学生信息插入数据库
        try:
            students.delete_student(self.db, self.cursor, student_id)
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
        student_major = self.student_major_input.text()
        student_photo = None
        if (self.photo):
            student_photo = self.photo

        if not (student_id and student_name and student_age and student_major):
            QMessageBox.warning(self, '输入错误', '所有字段都是必填的。')
            return

            # 将学生信息插入数据库
        try:
            students.add_student(self.db, self.cursor, student_id, student_name, student_age, student_major, student_photo)
            self.load_data()
            widget = QWidget()
            QMessageBox.information(widget, '信息', '添加成功')  # 触发的事件时弹出会话框
        except Exception as e:
            print(f"发生错误：{e}")
            return


    def change_student(self):
            oldID = self.student_id_input1.text()
            oldinfo = selects.select_student_baseinfo(self.db, self.cursor, oldID)
            if oldinfo == None:
                widget = QWidget()
                QMessageBox.information(widget, '信息', '学生不存在')
            else:
                self.changeWindow = Change_StudentWindow(self.db, self.cursor, oldinfo)
                if self.changeWindow.exec():
                    newID = self.changeWindow.get_entered_ID()
                    newName = self.changeWindow.get_entered_Name()
                    newAge = self.changeWindow.get_entered_Age()
                    newMajor = self.changeWindow.get_entered_Major()
                    newPhoto = self.changeWindow.get_entered_Photo()
                    students.change_student(self.db, self.cursor, oldID, 1, newName)
                    students.change_student(self.db, self.cursor, oldID, 2, newAge)
                    students.change_student(self.db, self.cursor, oldID, 3, newMajor)
                    students.change_student(self.db, self.cursor, oldID, 4, newPhoto)
                    students.changeid_student(self.db, self.cursor, oldID, newID)
                    widget = QWidget()
                    self.load_data()
                    QMessageBox.information(widget, '信息', '修改成功') #触发的事件时弹出会话框


class Change_StudentWindow(QDialog):
    def __init__(self, db, cursor, oldinfo):
        super().__init__()
        self.ID = oldinfo[0]
        self.name = oldinfo[1]
        self.age = oldinfo[2]
        self.major = oldinfo[3]
        self.photo = oldinfo[4]
        self.acceptflag = False
        self.setWindowTitle(f'请输入要修改的内容，不需要修改则留空')
        self.resize(320, 200)
        self.setWindowIcon(QIcon('./picture/logo.png'))
        self.init_ui()

    def init_ui(self):
        # 创建 QLabel 对象
        self.label1 = QLabel(f"从{self.ID}修改为：")
        self.label2 = QLabel(f"从{self.name}修改为：")
        self.label3 = QLabel(f"从{self.age}修改为：")
        self.label4 = QLabel(f"从{self.major}修改为：")

        # 创建 QLineEdit 对象
        self.input_box1 = QLineEdit(self)
        self.input_box1.setPlaceholderText("在此输入新的学号...")
        self.input_box2 = QLineEdit(self)
        self.input_box2.setPlaceholderText("在此输入新的姓名...")
        self.input_box3 = QLineEdit(self)
        self.input_box3.setPlaceholderText("在此输入新的年龄...")
        self.input_box4 = QLineEdit(self)
        self.input_box4.setPlaceholderText("在此输入新的专业...")

        # 创建上传照片按钮
        self.chooseButton = QPushButton('选择要上传的照片', self)
        self.chooseButton.clicked.connect(self.choosePhoto)

        # 创建确认按钮
        self.closeButton = QPushButton('确认', self)
        self.closeButton.clicked.connect(self.get_text)

        # 设置布局
        layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout1.addWidget(self.label1)
        layout1.addWidget(self.input_box1)
        layout2 = QHBoxLayout()
        layout2.addWidget(self.label2)
        layout2.addWidget(self.input_box2)
        layout3 = QHBoxLayout()
        layout3.addWidget(self.label3)
        layout3.addWidget(self.input_box3)
        layout4 = QHBoxLayout()
        layout4.addWidget(self.label4)
        layout4.addWidget(self.input_box4)
        layout5 = QHBoxLayout()
        layout5.addWidget(self.chooseButton)
        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.closeButton)
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addLayout(layout3)
        layout.addLayout(layout4)
        layout.addLayout(layout5)
        layout.addLayout(bottomLayout)
        self.setLayout(layout)

    def get_text(self):

        if (len(self.input_box1.text()) != 0):
            self.acceptflag = True
            self.ID = self.input_box1.text()
        if (len(self.input_box2.text()) != 0):
            self.acceptflag = True
            self.name = self.input_box2.text()
        if (len(self.input_box3.text()) != 0):
            try:
                self.age = int(self.input_box3.text())
                assert (self.age > 0)
                self.acceptflag = True
            except Exception as e:
                print(f"发生错误：{e}")
                widget = QWidget()
                QMessageBox.information(widget, '信息', '年龄不合法')  # 触发的事件时弹出会话框
        if (len(self.input_box4.text()) != 0):
            self.acceptflag = True
            self.major = self.input_box4.text()

        if self.acceptflag:
            self.accept()

    def choosePhoto(self):
        photo_path, _ = QFileDialog.getOpenFileName(self, "Select Photo", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if photo_path:
            # 读取图片并保存为二进制
            picture = open(photo_path, 'rb')
            pictureByte = picture.read()
            picture.close()
            self.photo = pictureByte
            self.acceptflag = True

    def get_entered_ID(self):
        return self.ID

    def get_entered_Name(self):
        return self.name

    def get_entered_Age(self):
        return self.age

    def get_entered_Major(self):
        return self.major

    def get_entered_Photo(self):
        return self.photo
