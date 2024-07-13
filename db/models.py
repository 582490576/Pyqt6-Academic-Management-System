"""

模型

"""
from db.db_handler import db_common, db_student, db_admin, db_teacher


# 公共类
class Common:
    def __init__(self):
        self.common = db_common

    # 登陆查询
    def login(self, username, password):
        return self.common.login(username, password)

    # 用户查询
    def user_exist(self, username):
        return self.common.user_exist(username)

    # 删除用户
    def user_delete(self, username):
        return self.common.db_delete(username)

    # 冻结用户
    def user_edit(self, username, state):
        return self.common.db_edit(username, state)

    # 获取课程数据
    def get_course(self):
        return self.common.db_get_course()

    # 获取虚拟学习人数
    def get_learning_quantity(self):
        return self.common.db_get_quantity()

    # 学生退课
    def stu_drop_course(self, course_name, stu_name):
        return self.common.db_stu_drop_course(course_name, stu_name)

    # 统计指定班级人数
    def count_class(self, class_name):
        return self.common.db_count_class(class_name)

    # 获取首页数据
    def get_home_data(self):
        return self.common.db_get_home_data()

    # 加载欢迎语
    def get_welcome_message(self):
        return self.common.db_get_welcome_message()


# 管理员
class Admin:
    def __init__(self):
        self.admin = db_admin.DbAdmin()

    # 数据预览
    def data_preview(self):
        return self.admin.db_data_preview()

    # 学生数据
    def stu_data(self):
        return self.admin.db_stu_data()

    # 学生查询
    def stu_query(self, text_query):
        return self.admin.db_stu_query(text_query)

    # 注册教师
    def add_teacher(self, username, password, salary):
        return self.admin.db_add_teacher(username, password, salary)

    # 获取教师数据
    def get_teacher_data(self):
        return self.admin.db_get_teacher_data()

    # 修改教师信息
    def change_teacher_salary(self, username, salary):
        return self.admin.db_change_teacher_salary(username, salary)

    def change_teacher_stata(self, username, state):
        return self.admin.db_change_teacher_stata(username, state)

    # 创建课程数据
    def add_course(self, name, price, teacher_name):
        return self.admin.db_add_course(name, price, teacher_name)

    # 删除课程
    def delete_course(self, course_data):
        return self.admin.db_delete_course(course_data)

    # 修改课程
    def edite_course(self, old_name, new_name, course_price, course_teacher):
        return self.admin.db_edite_course(old_name, new_name, course_price, course_teacher)

    # 发工资
    def get_paid(self, user_data):
        return self.admin.db_get_paid(user_data)

    # 获取流水数据
    def get_flow_data(self):
        return self.admin.db_get_flow_data()

    # 欢迎语
    def save_welcome(self, text):
        return self.admin.db_save_welcome(text)

    # 虚拟人数
    def save_ai(self, count):
        return self.admin.db_save_ai(count)


# 教师
class teacher:
    def __init__(self):
        self.teacher = db_teacher.DbTeacher()

    # 获取教师课程数据
    def get_teacher_course(self,user_name):
        return self.teacher.db_get_teacher_course(user_name)

    # 获取班级成员列表
    def get_class_member(self, course_name):
        return self.teacher.db_get_class_member(course_name)

    # 保存教师联系方式
    def save_number(self, teacher_name, number):
        return self.teacher.db_save_number(teacher_name, number)


# 学生
class student:
    def __init__(self):
        self.student = db_student.DbStudent()

    # 学生注册
    def register(self, username, password):
        return self.student.db_register(username, password)



    # 获取学生课程数据
    def get_stu_course(self, stu_name):
        return self.student.db_get_stu_course(stu_name)

    # 购买课程
    def purchase_courses(self, course_name, stu_name):
        return self.student.db_purchase_courses(course_name, stu_name)

    # 获取我的课程数据
    def get_my_course(self, course_name):
        return self.student.db_get_my_course(course_name)




