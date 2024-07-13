"""

    登录视图

"""
from PyQt6.QtCore import Qt

from gui.login import Ui_Form as LoginUiMixin
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox
import logging
import sys
from conf import settings
from interface import user_interface, student_interface
from core import admin_view, student_view, teacher_view

#  导入日志
user_logger = logging.getLogger('用户视图层')
# 定义角色
role = {
    '1': '学生',
    '2': '教师',
    '3': '管理员'
}


class LoginWindow(LoginUiMixin, QWidget):
    def __init__(self):
        super().__init__()
        self.teacher_window = None
        self.student_window = None
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)  # 隐藏边框
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # 透明窗口
        self.admin_window = None

    # 登录功能
    def login(self) -> bool:
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        # 是否为空
        if not username or not password:
            QMessageBox.warning(self, '警告', '账号或密码不能为空！')
            return False
        # 调用接口校验密码
        result = user_interface.user_login(username, password)
        if not result[0]:  # result -> (False,'错误信息')
            QMessageBox.warning(self, '警告', result[1])
            return False
        # 登入成功跳转界面 result -> (name,角色，状态)
        user_logger.info(f'{role[result[1]]}:{result[0]}登陆成功')
        # 定义用户信息元组
        use_tuple = (self, result[0], result[1])
        if result[1] == '1':
            # 启动学生界面
            self.close()
            self.student_window = student_view.StudentWindow(use_tuple)  # 传入
            self.student_window.show()
        elif result[1] == '2':
            # 启动教师界面
            self.close()
            self.teacher_window = teacher_view.TeacherWindow(use_tuple)  # 传入
            self.teacher_window.show()
        elif result[1] == '3':
            # 启动管理员界面
            self.close()
            self.admin_window = admin_view.AdminWindow(use_tuple)  # 传入
            self.admin_window.show()

    # 跳转注册页面
    def open_register_page(self):
        user_logger.debug('打开注册页面')
        self.stackedWidget.setCurrentIndex(1)

    # 跳转登入页面
    def open_login_page(self):
        self.stackedWidget.setCurrentIndex(0)

    # 注册功能
    def register(self) -> bool:
        username = self.lineEdit_5.text()
        password = self.lineEdit_6.text()
        confirm_password = self.lineEdit_7.text()
        if not username or not password or not confirm_password:
            QMessageBox.warning(self, '警告', '账号或密码不能为空！')
            return False
        if password != confirm_password:
            QMessageBox.warning(self, '警告', '两次密码不一致！')
            return False

        # 调用学生注册接口
        result = student_interface.stu_register(username, password)
        if not result[0]:
            QMessageBox.warning(self, '警告', result[1])
            return False
        QMessageBox.warning(self, '成功', result[1])
        user_logger.info(f"学生{username}注册成功！")
        return True


# 记录报错信息到控制台，调试用
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
    exc_info = traceback.format_exception(type(cls), exception, traceback)
    exc_str = ''.join(exc_info)
    # 记录日志
    logging.error(f"Uncaught exception: {exc_str}")


# 展示界面
def run():
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
