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


class Class_Table(QWidget):
    def __init__(self, db, cursor):
        super().__init__()
        self.db = db
        self.cursor = cursor
        self.setWindowTitle('课程')
        self.resize(500, 500)
        self.init_ui()

    def init_ui(self):
        info = selects.select_classes_all(self.db, self.cursor)
        leninfo = 3
        self.table = QTableWidget(len(info), leninfo)
        self.table.setHorizontalHeaderLabels(['课程号', '课程名', '学分'])

        # 填充表格数据
        for i in range(len(info)):
            for j in range(leninfo):
                item = QTableWidgetItem(str(info[i][j]))
                self.table.setItem(i, j, item)


        # 添加学生信息的输入框和按钮
        self.inputLayout = QHBoxLayout()
        self.class_id_input = QLineEdit()
        self.class_id_input.setPlaceholderText('课程号')
        self.class_name_input = QLineEdit()
        self.class_name_input.setPlaceholderText('课程名')
        self.class_age_input = QLineEdit()
        self.class_age_input.setPlaceholderText('学分')
        self.add_class_button = QPushButton('添加课程')
        self.add_class_button.clicked.connect(self.add_class)

        self.inputLayout.addWidget(QLabel('课程号:'))
        self.inputLayout.addWidget(self.class_id_input)
        self.inputLayout.addWidget(QLabel('课程名:'))
        self.inputLayout.addWidget(self.class_name_input)
        self.inputLayout.addWidget(QLabel('学分:'))
        self.inputLayout.addWidget(self.class_age_input)
        self.inputLayout.addWidget(self.add_class_button)


        self.inputLayout1 = QHBoxLayout()
        self.class_id_input1 = QLineEdit()
        self.class_id_input1.setPlaceholderText('课程号')
        self.del_class_button = QPushButton('删除课程')
        self.del_class_button.clicked.connect(self.delete_class)
        self.change_class_Button = QPushButton('修改课程信息', self)
        self.change_class_Button.clicked.connect(self.change_class)


        self.inputLayout1.addWidget(QLabel('课程号:'))
        self.inputLayout1.addWidget(self.class_id_input1)
        self.inputLayout1.addWidget(self.del_class_button)
        self.inputLayout1.addWidget(self.change_class_Button)


        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addLayout(self.inputLayout)
        layout.addLayout(self.inputLayout1)
        self.setLayout(layout)


    def load_data(self):
        info = selects.select_classes_all(self.db, self.cursor)
        leninfo = 3
        headers = ['课程号', '课程名', '学分']


        self.table.setRowCount(len(info))
        self.table.setColumnCount(leninfo)
        self.table.setHorizontalHeaderLabels(headers)

        for i in range(len(info)):
            for j in range(leninfo):
                item = QTableWidgetItem(str(info[i][j]))
                self.table.setItem(i, j, item)

    def delete_class(self):
        class_id = self.class_id_input1.text()
        #print(class_id)

        if not (class_id):
            QMessageBox.warning(self, '输入为空')
            return

        # 将学生信息插入数据库
        try:
            classes.delete_class(self.db, self.cursor, class_id)
            self.load_data()
            widget = QWidget()
            QMessageBox.information(widget, '信息', '删除成功')  # 触发的事件时弹出会话框
        except Exception as e:
            print(f"发生错误：{e}")
            return

    def add_class(self):
        class_id = self.class_id_input.text()
        class_name = self.class_name_input.text()
        class_age = self.class_age_input.text()


        if not (class_id and class_name and class_age):
            QMessageBox.warning(self, '输入错误', '所有字段都是必填的。')
            return

            # 将学生信息插入数据库
        try:
            classes.add_class(self.db, self.cursor, class_id, class_name, class_age)
            self.load_data()
            widget = QWidget()
            QMessageBox.information(widget, '信息', '添加成功')  # 触发的事件时弹出会话框

        except Exception as e:
            print(f"发生错误：{e}")
            return


    def change_class(self):
            # 如果用户点击确认按钮，则获取输入的文本
            oldID = self.class_id_input1.text()
            oldinfo = selects.select_class_ID(self.db, self.cursor, oldID)
            if oldinfo == None:
                widget = QWidget()
                QMessageBox.information(widget, '信息', '学生不存在')
            else:
                self.changeWindow = Change_classWindow(self.db, self.cursor, oldinfo)
                if self.changeWindow.exec():
                    newID = self.changeWindow.get_entered_ID()
                    newName = self.changeWindow.get_entered_Name()
                    newAge = self.changeWindow.get_entered_Age()

                    classes.change_class(self.db, self.cursor, oldID, 1, newName)
                    classes.change_class(self.db, self.cursor, oldID, 2, newAge)
                    classes.changeid_class(self.db, self.cursor, oldID, newID)
                    widget = QWidget()
                    self.load_data()
                    QMessageBox.information(widget, '信息', '修改成功') #触发的事件时弹出会话框


class Change_classWindow(QDialog):
    def __init__(self, db, cursor, oldinfo):
        super().__init__()
        self.ID = oldinfo[0]
        self.name = oldinfo[1]
        self.age = oldinfo[2]

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

        # 创建 QLineEdit 对象
        self.input_box1 = QLineEdit(self)
        self.input_box1.setPlaceholderText("在此输入新的学号...")
        self.input_box2 = QLineEdit(self)
        self.input_box2.setPlaceholderText("在此输入新的姓名...")
        self.input_box3 = QLineEdit(self)
        self.input_box3.setPlaceholderText("在此输入新的年龄...")


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

        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.closeButton)
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addLayout(layout3)

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


        if self.acceptflag:
            self.accept()


    def get_entered_ID(self):
        return self.ID

    def get_entered_Name(self):
        return self.name

    def get_entered_Age(self):
        return self.age


