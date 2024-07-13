"""

    学生视图

"""
import re
from datetime import datetime

from PyQt6.QtGui import QPixmap
from lib import common
from gui.student import Ui_Form as StudentUiMixin
from interface import student_interface
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox, QPushButton, QHBoxLayout, QInputDialog, QLineEdit
import logging
import sys
from conf import settings

#  导入日志
user_logger = logging.getLogger('用户视图层')


class StudentWindow(StudentUiMixin, QWidget):
    def __init__(self, use_tuple):
        super(StudentWindow, self).__init__()
        self.stu_course = None
        self.setupUi(self)
        self.student_interface = student_interface
        # 获取用户信息
        self.use_tuple = use_tuple
        self.open_home_page()
        self.set_img()
        self.show_welcome_message()

    # 打开首页
    def open_home_page(self):
        result = self.student_interface.get_home_data()
        # 显示数据
        self.label_14.setText(result[0][0])
        self.label_15.setText(result[0][1])
        self.label_20.setText(result[1][0])
        self.label_21.setText(result[1][1])
        self.label_23.setText(result[2][0])
        self.label_24.setText(result[2][1])
        self.label_32.setText(result[3][0])
        self.label_33.setText(result[3][1])
        self.label_26.setText(result[4][0])
        self.label_27.setText(result[4][1])
        self.label_29.setText(result[5][0])
        self.label_30.setText(result[5][1])
        self.stackedWidget.setCurrentIndex(0)

    # 课程列表页
    def open_course_page(self):
        self.stackedWidget.setCurrentIndex(1)
        # 获取课程数据
        result = self.student_interface.get_course()
        self.stu_course = self.student_interface.get_stu_course(self.use_tuple[1])
        if not result[0]:
            self.tableWidget_2.clearContents()
            self.tableWidget_2.setRowCount(0)
            return
        self.show_table_data(self.tableWidget_2, result[1], 1)

    # 我的列表
    def open_mycourse_page(self):
        self.stackedWidget.setCurrentIndex(2)
        # 获取我的课程数据
        result = self.student_interface.get_my_course(self.use_tuple[1])
        if not result[0]:
            self.tableWidget_3.clearContents()
            self.tableWidget_3.setRowCount(0)
            return
        self.show_table_data(self.tableWidget_3, result[1], 2)

    # 输出到列表
    def show_table_data(self, table, data_list, _op):
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
                # 添加按钮
            self.set_buttons(row_idx, table, data_list, _op)

    # 生成按钮
    def set_buttons(self, row_idx, table, data_list, _op):
        """
        生成编辑按钮并绑定曹信号
        :param row_idx: 行索引
        :param table: 表格对象
        :param data_list: 数据列表
        :param _op: 1 = 课程列表按钮设计 ，2 = 已购买的课程列表按钮设计
        :return:
        """
        if _op == 1:
            if data_list[row_idx][0] in self.stu_course:
                edit_button = QPushButton("已购买")
                edit_button.setStyleSheet("""
                                    QPushButton{
                            border-radius:15px;
                            color: rgb(255, 255, 255);
                            background-color: rgb(215, 215, 215);
                        }
                        
                        QPushButton:hover{
                            background-color: rgb(235, 235, 235);
                        }
                        QPushButton:pressed{
                            background-color: rgb(185,185,185);
                        }
                        """)
                edit_button.setMaximumSize(70, 18)
            else:
                edit_button = QPushButton("购买")
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
                edit_button.clicked.connect(lambda: self.click_1(data_list[row_idx]))
            # 创建容器
            layout = QHBoxLayout()
            layout.addWidget(edit_button)
            widget = QWidget()
            widget.setLayout(layout)
            # 将布局的容器添加到表格的单元格中
            table.setCellWidget(row_idx, len(data_list[0]), widget)

        else:
            # 已购买的课程
            edit_button = QPushButton("退课")
            edit_button.setStyleSheet("""
                                    QPushButton{
                            border-radius:15px;
                            color: rgb(255, 255, 255);
                            background-color: rgb(215, 215, 215);
                        }
                        
                        QPushButton:hover{
                            background-color: rgb(235, 235, 235);
                        }
                        QPushButton:pressed{
                            background-color: rgb(185,185,185);
                        }
                        """)
            edit_button.setMaximumSize(70, 18)
            edit_button.clicked.connect(lambda: self.click_2(data_list[row_idx]))
            layout = QHBoxLayout()
            layout.addWidget(edit_button)
            widget = QWidget()
            widget.setLayout(layout)
            table.setCellWidget(row_idx, len(data_list[0]), widget)

    # 按钮方法
    def click_1(self, data_list):
        reply = QMessageBox.question(
            self,  # 父窗口
            '警告',  # 窗口标题
            f'是否购买课程 {data_list[0]} ？',  # 消息内容
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,  # 按钮组合
            QMessageBox.StandardButton.No  # 默认按钮
        )
        if reply == QMessageBox.StandardButton.Yes:
            result = self.student_interface.purchase_courses(data_list[0], self.use_tuple[1])
            if result:
                QMessageBox.warning(self, '成功', '购买成功！')
                user_logger.info(f"用户{self.use_tuple[1]}购买课程{data_list[0]}成功！")
                self.pushButton_2.click()
            else:
                QMessageBox.warning(self, '失败', '购买失败！')

    def click_2(self, data_list):
        reply = QMessageBox.question(
            self,  # 父窗口
            '警告',  # 窗口标题
            f'是否将课程 {data_list[0]} 退课？',  # 消息内容
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,  # 按钮组合
            QMessageBox.StandardButton.No  # 默认按钮
        )
        if reply == QMessageBox.StandardButton.Yes:
            result = self.student_interface.drop_course(data_list[0], self.use_tuple[1])
            if result:
                QMessageBox.warning(self, '成功', '退课成功！')
                user_logger.info(f"用户{self.use_tuple[1]}退出课程{data_list[0]}成功！")
                self.pushButton_7.click()
            else:
                QMessageBox.warning(self, '失败', '退课失败！')

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

    # 加载欢迎语
    def show_welcome_message(self):
        result = self.student_interface.show_welcome_message()
        if result[0]:
            self.label_3.setText(result[1])
