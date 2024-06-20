import sys
import pymysql
from PyQt6.QtWidgets import QPushButton, QMessageBox, QApplication, QWidget
import login


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = login.LoginWindow()
    window.show()
    sys.exit(app.exec())