import sys
import io
import selects
import classes
import students
import scores
import prizes
import punishments
from PyQt6.QtWidgets import QPushButton, QMessageBox, QApplication, QVBoxLayout, QTableWidget, QTableWidgetItem, \
    QWidget, QHBoxLayout
from PyQt6.QtWidgets import QLineEdit, QDialog, QLabel, QFileDialog
from PyQt6.QtCore import QByteArray, Qt
from PyQt6.QtGui import QIcon, QPixmap, QImage
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QByteArray, QSize, Qt
from PyQt6.QtWidgets import QLabel

class Search_Stu(QDialog):
    def __init__(self, db, cursor):
        super().__init__()
        self.db = db
        self.cursor = cursor
        self.ID = ''
        self.setWindowTitle('输入需要查询的学生学号')
        self.resize(320, 200)
        self.init_ui()

    def init_ui(self):

        # 创建 QLineEdit 对象
        self.input_box1 = QLineEdit(self)
        self.input_box1.setPlaceholderText("在此输入学号...")

        # 创建确认按钮
        self.closeButton = QPushButton('确认', self)
        self.closeButton.clicked.connect(self.get_text)

        # 设置布局
        layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout1.addWidget(self.input_box1)
        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.closeButton)
        layout.addLayout(layout1)
        layout.addLayout(bottomLayout)
        self.setLayout(layout)

    def get_text(self):
        self.acceptflag = False
        if (len(self.input_box1.text()) != 0):
            self.ID = self.input_box1.text()
            info = selects.select_student_baseinfo(self.db, self.cursor, self.ID)
            if info == None:
                widget = QWidget()
                QMessageBox.information(widget, '信息', '学生不存在')  # 触发的事件时弹出会话框
            else:
                self.res = ResultWindow(self.db, self.cursor, self.ID)
                self.res.show()

        if self.acceptflag:
            self.accept()

    def get_entered_ID(self):
        return self.ID

class ResultWindow(QWidget):
        def __init__(self, db, cursor, id):
            super().__init__()
            self.db = db
            self.cursor = cursor
            self.id = id
            info = selects.select_student_baseinfo(self.db, self.cursor, self.id)
            self.name = info[1]
            self.age = info[2]
            self.major = info[3]
            self.photo = info[4]
            self.setWindowTitle('学生详细信息')
            self.resize(720, 540)
            self.init_ui()

        def init_ui(self):
            scoreinfo = selects.select_student_score(self.db, self.cursor, self.id)
            punishinfo = selects.select_student_punish(self.db, self.cursor, self.id)
            prizeinfo = selects.select_student_prizes(self.db, self.cursor, self.id)
            if (len(scoreinfo) != 0):
                total_points = scores.get_total_points(self.db, self.cursor, self.id)
                avg_points = scores.get_avg_points(self.db, self.cursor, self.id)
            else:
                total_points = 0

            # 创建 QLabel 对象
            self.label1 = QLabel(f"学号：{self.id}")
            self.label2 = QLabel(f"姓名：{self.name}")
            self.label3 = QLabel(f"年龄：{self.age}")
            self.label4 = QLabel(f"专业：{self.major}")
            self.label5 = QLabel(f"当前已获总学分：{total_points[0]}")
            self.label7 = QLabel(f"平均分：{avg_points[0]}")
            try:
                if(self.photo):
                    image = QImage.fromData(QByteArray(self.photo))
                    pixmap = QPixmap(image)

                    # 将图片大小限制为 200x200 像素
                    fixed_size = QSize(200, 200)
                    scaled_pixmap = pixmap.scaled(fixed_size, Qt.AspectRatioMode.KeepAspectRatio,
                                                  Qt.TransformationMode.SmoothTransformation)

                    self.label6 = QLabel(self)
                    self.label6.setPixmap(scaled_pixmap)

                else:
                    self.label6 = None
            except Exception as e:
                print(f"发生错误：{e}")
                return

            # 创建表格
            self.table1 = QTableWidget(len(scoreinfo), 4)
            self.table1.setHorizontalHeaderLabels(['课程号','课程名', '学分', '成绩'])
            # 填充表格数据
            for i in range(len(scoreinfo)):
                for j in range(len(scoreinfo[i])):
                    item = QTableWidgetItem(str(scoreinfo[i][j]))
                    self.table1.setItem(i, j, item)
            # 创建表格
            self.table2 = QTableWidget(len(prizeinfo), 2)
            self.table2.setHorizontalHeaderLabels(['奖项', '时间'])
            # 填充表格数据
            for i in range(len(prizeinfo)):
                for j in range(1,3):
                    item = QTableWidgetItem(str(prizeinfo[i][j]))
                    self.table2.setItem(i, j-1, item)

            # 创建表格
            self.table3 = QTableWidget(len(punishinfo), 2)
            self.table3.setHorizontalHeaderLabels(['惩罚', '时间'])
            # 填充表格数据
            for i in range(len(punishinfo)):
                for j in range(1,3):
                    item = QTableWidgetItem(str(punishinfo[i][j]))
                    self.table3.setItem(i, j-1, item)

            # 创建关闭按钮
            self.closeButton = QPushButton('修改信息', self)
            self.closeButton.clicked.connect(self.change)

            # 设置布局
            layout = QVBoxLayout()
            layout_base = QHBoxLayout()
            layout_base1 = QVBoxLayout()


            layout_base.addWidget(self.label6)
            layout.addLayout(layout_base)

            layout1 = QHBoxLayout()
            layout1.addWidget(self.label1)
            layout1.addWidget(self.label2)
            layout2 = QHBoxLayout()
            layout2.addWidget(self.label3)
            layout2.addWidget(self.label4)
            layout3 = QHBoxLayout()
            layout3.addWidget(self.label7)
            layout3.addWidget(self.label5)


            layout_base1.addLayout(layout1)
            layout_base1.addLayout(layout2)
            layout_base1.addLayout(layout3)
            layout_base.addLayout(layout_base1)

            layout.addWidget(self.table1)
            table_layout = QHBoxLayout()
            table_layout.addWidget(self.table2)
            table_layout.addWidget(self.table3)
            layout.addLayout(table_layout)
            bottomLayout = QHBoxLayout()
            bottomLayout.addWidget(self.closeButton)
            layout.addLayout(bottomLayout)
            self.setLayout(layout)


        def change(self):
                # 如果用户点击确认按钮，则获取输入的文本
                oldID = self.id
                oldinfo = selects.select_student_baseinfo(self.db, self.cursor, oldID)
                if oldinfo == None:
                    widget = QWidget()
                    QMessageBox.information(widget, '警告', '学生不存在')
                else:
                    self.changeWindow = Change_StudentWindow(self.db, self.cursor, oldinfo)
                    if self.changeWindow.exec():
                        newAge = self.changeWindow.get_entered_Age()
                        newMajor = self.changeWindow.get_entered_Major()
                        newPhoto = self.changeWindow.get_entered_Photo()
                        students.change_student(self.db, self.cursor, oldID, 2, newAge)
                        students.change_student(self.db, self.cursor, oldID, 3, newMajor)
                        students.change_student(self.db, self.cursor, oldID, 4, newPhoto)
                        widget = QWidget()
                        self.window = ResultWindow(self.db, self.cursor, oldID)
                        self.window.show()
                        self.close()
                        QMessageBox.information(widget, '成功', '修改成功')  # 触发的事件时弹出会话框

class Change_StudentWindow(QDialog):
            def __init__(self, db, cursor, oldinfo):
                super().__init__()
                self.ID = oldinfo[0]
                self.name = oldinfo[1]
                self.age = oldinfo[2]
                self.major = oldinfo[3]
                self.photo = oldinfo[4]
                self.acceptflag = False
                self.setWindowTitle(f'输入要修改的内容')
                self.resize(320, 200)
                self.init_ui()

            def init_ui(self):
                # 创建 QLabel 对象
                self.label3 = QLabel(f"原年龄{self.age}：")
                self.label4 = QLabel(f"原专业{self.major}：")

                # 创建 QLineEdit 对象
                self.input_box3 = QLineEdit(self)
                self.input_box3.setPlaceholderText("输入新的年龄...")
                self.input_box4 = QLineEdit(self)
                self.input_box4.setPlaceholderText("输入新的专业...")

                # 创建上传照片按钮
                self.chooseButton = QPushButton('选择新的照片', self)
                self.chooseButton.clicked.connect(self.choosePhoto)

                # 创建确认按钮
                self.closeButton = QPushButton('更改', self)
                self.closeButton.clicked.connect(self.get_text)

                # 设置布局
                layout = QVBoxLayout()
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
                layout.addLayout(layout3)
                layout.addLayout(layout4)
                layout.addLayout(layout5)
                layout.addLayout(bottomLayout)
                self.setLayout(layout)

            def get_text(self):

                if (len(self.input_box3.text()) != 0):
                    try:
                        self.age = int(self.input_box3.text())
                        assert (self.age > 0)
                        self.acceptflag = True
                    except Exception as e:
                        print(f"发生错误：{e}")
                        widget = QWidget()
                        QMessageBox.information(widget, '警告', '年龄不合法')
                if (len(self.input_box4.text()) != 0):
                    self.acceptflag = True
                    self.major = self.input_box4.text()

                if self.acceptflag:
                    self.accept()

            def choosePhoto(self):
                photo_path, _ = QFileDialog.getOpenFileName(self, "Select Photo", "",
                                                            "Image Files (*.png *.jpg *.jpeg *.bmp)")
                if photo_path:
                    # 读取图片并保存为二进制
                    picture = open(photo_path, 'rb')
                    pictureByte = picture.read()
                    picture.close()
                    self.photo = pictureByte
                    self.acceptflag = True


            def get_entered_Age(self):
                return self.age

            def get_entered_Major(self):
                return self.major

            def get_entered_Photo(self):
                return self.photo