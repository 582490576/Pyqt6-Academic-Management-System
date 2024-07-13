"""

    管理员视图

"""
import re
from datetime import datetime

from PyQt6.QtGui import QPixmap

from gui.admin import Ui_Form as AdminUiMixin
from interface import admin_interface
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox, QPushButton, QHBoxLayout, QInputDialog, QLineEdit
import logging
import sys
from conf import settings
from lib import common

#  导入日志
user_logger = logging.getLogger('用户视图层')


class AdminWindow(AdminUiMixin, QWidget):
    def __init__(self, use_tuple):
        super(AdminWindow, self).__init__()
        self.user_data = None
        self.setupUi(self)
        self.admin_interface = admin_interface
        # 获取用户信息
        self.use_tuple = use_tuple
        self.open_home_page()
        self.set_img()

    # 打开首页
    def open_home_page(self):
        # 调用接口获取预览数据
        result = self.admin_interface.data_preview()
        if not result:
            self.stackedWidget.setCurrentIndex(0)
            user_logger.info(f"error | 错误日志! -- {result}")
        # 显示数据
        self.label_15.setText(result[1])
        self.label_21.setText(result[2])
        self.label_24.setText(result[3])
        self.label_33.setText(result[4])
        self.label_27.setText(result[5])
        self.label_30.setText(result[6])
        self.stackedWidget.setCurrentIndex(0)

    # 初始化学生管理页
    def open_stu_page(self):
        self.pushButton_11.click()
        self.stackedWidget.setCurrentIndex(1)

    # 显示学生表格
    def stu_all(self, op=1):
        """
        显示全部学生表格
        :param op: 1 = 全部学生，2 = 购买课程的学生，3 = 未购买课程的学生
        :return:
        """
        result = self.admin_interface.get_data_stu(op)
        if not result[0]:
            self.tableWidget.clearContents()
            self.tableWidget.setRowCount(0)
            return
        self.show_table_data(self.pushButton_11, self.tableWidget, result, 1)

    # 购买课程的学生
    def stu_paid(self):
        self.stu_all(2)

    # 未购买课程的学生
    def stu_notpaid(self):
        self.stu_all(3)

    # 查询指定账号的学生
    def stu_query(self):
        self.stackedWidget.setCurrentIndex(1)
        text_query = self.lineEdit.text()
        if not text_query:
            QMessageBox.warning(self, '警告', '输入为空！')
            return
        result = self.admin_interface.stu_query(text_query)
        if not result[0]:
            self.tableWidget.clearContents()
            self.tableWidget.setRowCount(0)
            user_logger.info(f"error | 错误日志! -- {result[1]}")
            self.lineEdit.clear()
            return
        # 生成列表
        self.show_table_data(self.pushButton_11, self.tableWidget, result, 1)
        self.lineEdit.clear()

    # 输出到列表
    def show_table_data(self, pushbutton, table, data_list, _op):
        # 清空表格中的现有内容
        table.clearContents()
        table.setRowCount(len(data_list))

        # 遍历数据列表，每个元素是一个元组
        for row_idx, data_tuple in enumerate(data_list):
            # 遍历元组中的每个元素，每个元素是一个列的值
            for col_idx, data in enumerate(data_tuple):
                # 如果数据是datetime类型，格式化为字符串
                if isinstance(data, datetime):
                    data = data.strftime('%Y-%m-%d')
                # 创建表格项
                item = QTableWidgetItem(str(data))
                # 将项添加到表格的对应位置
                table.setItem(row_idx, col_idx, item)
            if _op != 5:
                # 添加按钮
                self.set_buttons(pushbutton, row_idx, table, data_list, _op)

    # 生成按钮
    def set_buttons(self, pushbutton, row_idx, table, data_list, _op):
        """
        生成编辑按钮并绑定曹信号
        :param pushbutton:
        :param row_idx: 行索引
        :param table: 表格对象
        :param data_list: 数据列表
        :param _op: 1 = 学生列表 ，2 = 教师列表 ， 3 = 课程列表，4 = 发工资列
        :return:
        """
        # 创建编辑按钮
        if _op == 4:
            edit_button = QPushButton("发工资")
            edit_button.setStyleSheet("QPushButton{\n"
                                      "    border-radius:15px;\n"
                                      "    color: rgb(255, 255, 255);\n"
                                      "    background-color: rgb(0, 170, 127);\n"
                                      "}\n"
                                      "\n"
                                      "QPushButton:hover{\n"
                                      "    background-color: rgb(0, 194, 142);\n"
                                      "}\n"
                                      "\n"
                                      "QPushButton:pressed{\n"
                                      "    background-color: rgb(0, 141, 103);\n"
                                      "}")
            edit_button.setMaximumSize(70, 18)
            # 连接编辑按钮的点击事件
            edit_button.clicked.connect(lambda: self.click_edit(data_list[row_idx], pushbutton, _op))
            layout = QHBoxLayout()
            layout.addWidget(edit_button)
            widget = QWidget()
            widget.setLayout(layout)
            # 将布局的容器添加到表格的单元格中
            table.setCellWidget(row_idx, len(data_list[0]), widget)
        else:
            edit_button = QPushButton("编辑")
            edit_button.setStyleSheet("QPushButton{\n"
                                      "    border-radius:15px;\n"
                                      "    color: rgb(255, 255, 255);\n"
                                      "    background-color: rgb(0, 170, 127);\n"
                                      "}\n"
                                      "\n"
                                      "QPushButton:hover{\n"
                                      "    background-color: rgb(0, 194, 142);\n"
                                      "}\n"
                                      "\n"
                                      "QPushButton:pressed{\n"
                                      "    background-color: rgb(0, 141, 103);\n"
                                      "}")
            edit_button.setMaximumSize(70, 18)
            # 连接编辑按钮的点击事件
            edit_button.clicked.connect(lambda: self.click_edit(data_list[row_idx], pushbutton, _op))
            # 创建删除按钮
            delete_button = QPushButton("删除")
            delete_button.setStyleSheet("QPushButton{"
                                        "color: rgb(255, 255, 255);"
                                        "border-radius:10px; background-color: rgb(166, 166, 166);}"
                                        "QPushButton:hover{ background-color: rgb(232, 232, 232);}"
                                        "QPushButton:pressed{"
                                        "background-color: rgb(166, 166, 166);}")
            delete_button.setMaximumSize(70, 18)
            # 连接删除按钮的点击事件
            delete_button.clicked.connect(lambda: self.click_delete(data_list[row_idx], pushbutton, _op))
            # 创建容器
            widget = QWidget()
            layout = QHBoxLayout(widget)
            layout.addWidget(edit_button)
            layout.addWidget(delete_button)
            table.setCellWidget(row_idx, len(data_list[0]), widget)

    # 编辑按钮的槽函数
    def click_edit(self, user_data, pushbutton, _op):
        if _op == 1:
            self.frozen_delete(user_data, pushbutton, 1)
        elif _op == 2:
            self.edit_teacher(user_data)
        elif _op == 3:
            self.edite_course_page(user_data)
        elif _op == 4:
            self.get_paid(user_data)

    # 删除按钮的槽函数
    def click_delete(self, user_data, pushbutton, _op):
        if _op == 3:
            self.delete(user_data, pushbutton, self.admin_interface.delete_course)
        else:
            self.frozen_delete(user_data, pushbutton)

    # 删除通用方法
    def delete(self, user_data, pushbutton, interface):
        reply = QMessageBox.question(
            self,  # 父窗口
            '警告',  # 窗口标题
            f'是否删除 {user_data[0]} ？',  # 消息内容
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,  # 按钮组合
            QMessageBox.StandardButton.No  # 默认按钮
        )
        if reply == QMessageBox.StandardButton.Yes:
            interface(user_data[0])
            QMessageBox.warning(self, '成功', '删除成功！')
            user_logger.info(f"删除{user_data[0]}成功！")
            pushbutton.click()

    # 定义冻结和删除学生的功能
    def frozen_delete(self, user_data, pushbutton, _op=0):
        """
        定义编辑和删除学生的功能
        :param pushbutton: 点击按钮
        :param user_data: 用户信息表
        :param _op: 1为编辑、0为删除
        :return:
        """
        if _op == 0:
            self.delete(user_data, pushbutton, self.admin_interface.delete_stu)
        else:
            if user_data[2] == '正常':
                state = '冻结'
            else:
                state = '解冻'
            reply = QMessageBox.question(
                self,
                '编辑',
                f'是否{state} {user_data[0]} ？',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.admin_interface.edit_stu(user_data)
                QMessageBox.warning(self, '成功', f'{state}成功！')
                user_logger.info(f"{state}{user_data[0]}成功！")
                pushbutton.click()

    # 课程管理页
    def open_course_page(self):
        self.stackedWidget.setCurrentIndex(2)
        self.tableWidget_2.clearContents()
        self.tableWidget_2.setRowCount(0)
        # 获取教师数据
        result = self.admin_interface.get_course()
        if not result[0]:
            self.tableWidget_2.clearContents()
            self.tableWidget_2.setRowCount(0)
            return
        self.show_table_data(self.pushButton_7, self.tableWidget_2, result[1], 3)

    # 打开创建课程页面
    def open_addcourse_page(self):
        self.stackedWidget.setCurrentIndex(6)
        self.lineEdit_5.clear()
        self.lineEdit_6.clear()
        self.lineEdit_7.clear()

    # 创建课程
    def add_course(self):
        name = self.lineEdit_5.text()
        price = self.lineEdit_6.text()
        teacher = self.lineEdit_7.text()
        if not name or not price or not teacher:
            QMessageBox.warning(self, '警告', '信息不能为空！')
            return False
        # 调用接口
        result = self.admin_interface.add_course(name, price, teacher)
        if not result[0]:
            QMessageBox.warning(self, '警告', result[1])
            return False
        QMessageBox.warning(self, '成功', result[1])
        user_logger.info(f"课程{name}添加成功！")
        self.lineEdit_5.clear()
        self.lineEdit_6.clear()
        self.lineEdit_7.clear()

    # 打开课程编辑页
    def edite_course_page(self, user_data):
        self.user_data = user_data
        self.stackedWidget.setCurrentIndex(9)
        self.lineEdit_12.setText(user_data[0])
        self.lineEdit_13.setText(str(user_data[1]))
        self.lineEdit_14.setText(user_data[3])

    # 课程编辑方法
    def edite_course(self):
        course_name = self.lineEdit_12.text()
        course_price = self.lineEdit_13.text()
        course_teacher = self.lineEdit_14.text()
        result = self.admin_interface.edite_course(self.user_data, course_name, course_price, course_teacher)
        if not result[0]:
            QMessageBox.warning(self, '警告', result[1])
        else:
            QMessageBox.warning(self, '成功', result[1])

    # 跳转教师管理页
    def open_teacher_page(self):
        self.stackedWidget.setCurrentIndex(3)
        self.tableWidget_3.clearContents()
        self.tableWidget_3.setRowCount(0)
        result = self.admin_interface.get_teacher_data()
        if not result[0]:
            self.tableWidget_3.clearContents()
            self.tableWidget_3.setRowCount(0)
            return
        self.show_table_data(self.pushButton_3, self.tableWidget_3, result[1], 2)

    # 打开注册教师页面
    def open_addteacher_page(self):
        self.stackedWidget.setCurrentIndex(7)

    # 添加教师
    def add_teacher(self):
        username = self.lineEdit_8.text()
        password = self.lineEdit_9.text()
        salary = self.lineEdit_10.text()
        # 是否为空
        if not username or not password or not salary:
            QMessageBox.warning(self, '警告', '信息不能为空！')
            return False
        # 调用接口验证
        result = self.admin_interface.add_teacher(username, password, salary)
        if not result[0]:
            QMessageBox.warning(self, '警告', result[1])
            return False
        QMessageBox.warning(self, '警告', result[1])
        user_logger.info(f"教师{username}注册成功！")
        self.lineEdit_8.clear()
        self.lineEdit_9.clear()
        self.lineEdit_10.clear()

    # 打开教师编辑页
    def edit_teacher(self, user_data):
        self.user_data = user_data
        self.stackedWidget.setCurrentIndex(8)
        self.lineEdit_11.setText(str(user_data[2]))
        if user_data[3] == '正常':
            self.checkBox.setText('是否冻结')
        else:
            self.checkBox.setText('是否解冻')

    # 教师修改
    def change_teacher(self):
        new_salary = self.lineEdit_11.text()
        state = self.checkBox.isChecked()
        result = self.admin_interface.change_teacher(self.user_data, new_salary, state)
        if not result[0]:
            QMessageBox.warning(self, '警告', result[1])
        else:
            QMessageBox.warning(self, '成功', result[1])
            self.pushButton_3.click()

    # 财务页
    def open_money_page(self):
        self.stackedWidget.setCurrentIndex(4)
        # 发工资页
        self.tableWidget_4.clearContents()
        self.tableWidget_4.setRowCount(0)
        result = self.admin_interface.get_teacher_data(1)
        if not result[0]:
            self.tableWidget_4.clearContents()
            self.tableWidget_4.setRowCount(0)
            return
        self.show_table_data(None, self.tableWidget_4, result[1], 4)
        # 流水页
        self.tableWidget_5.clearContents()
        self.tableWidget_5.setRowCount(0)
        result = self.admin_interface.get_flow_data()
        if not result[0]:
            self.tableWidget_5.clearContents()
            self.tableWidget_5.setRowCount(0)
            return
        self.show_table_data(None, self.tableWidget_5, result[1], 5)

    # 发工资
    def get_paid(self, user_data):
        reply = QMessageBox.question(
            self,
            '编辑',
            f'是否给教师{user_data[0]} 发工资 ？',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            result = self.admin_interface.get_paid(user_data)
            if result:
                QMessageBox.warning(self, '成功', '成功！')
                self.open_money_page()
                user_logger.info(f"给教师{user_data[0]}发工资成功！")
            else:
                QMessageBox.warning(self, '警告', '失败！')

    # 设置页
    def open_setting_page(self):
        self.stackedWidget.setCurrentIndex(5)
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()

    # 虚拟人数
    def save_ai(self):
        self.stackedWidget.setCurrentIndex(5)
        text = self.lineEdit_3.text()
        result = self.admin_interface.save_ai(text)
        if result[0]:
            QMessageBox.warning(self, '成功',result[1])
        else:
            QMessageBox.warning(self, '警告', result[1])

    # 欢迎语
    def save_welcome(self):
        text = self.lineEdit_2.text()
        result = self.admin_interface.save_welcome(text)
        if result:
            QMessageBox.warning(self, '成功','保存成功！')
        else:
            QMessageBox.warning(self, '警告', '保存失败！')

    # 退出
    def login_out(self):
        self.close()
        # 显示登录窗口
        self.use_tuple[0].show()
        user_logger.info(f"用户{self.use_tuple[1]} 退出")

    # 加载图片
    def set_img(self):
        imgs_dir = common.get_imgs_dirname()
        img = QPixmap(rf"{imgs_dir}/imgs/1.jpg").scaled(self.label_2.size())
        self.label_2.setPixmap(img)



# 记录报错信息到控制台，调试用
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
    exc_info = traceback.format_exception(type(cls), exception, traceback)
    exc_str = ''.join(exc_info)
    # 记录日志
    logging.error(f"Uncaught exception: {exc_str}")
