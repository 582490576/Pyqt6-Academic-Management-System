"""
学生接口

"""
from db import models
from lib import common
import re


# 学生注册
def stu_register(username, password) -> tuple:
    username = username.strip()
    password = password.strip()
    if re.match(r'^[\u4e00-\u9fa5a-zA-Z0-9]{2,8}$', username) is None:
        return False, '账号不符合规定！'
    if re.match(r'^[0-9a-zA-Z]{6,8}$', password) is None:
        return False, '密码不符合规定！'
    # 用户查重
    if models.Common().user_exist(username):
        return False, '用户名已存在！'

    # 加密
    password = common.pw_to_sha512(password)

    # 调用学生模版写入注册信息
    stu = models.student()
    if stu.register(username, password):
        return True, '注册成功'
    return False, '出现错误，注册失败！'


# 获取首页数据
def get_home_data() -> list:
    db_common = models.Common()
    # 课程数据
    result = db_common.get_home_data()
    # 虚拟人数
    count = db_common.get_learning_quantity()
    # 清洗补充数据到6条
    home_data = []
    if result[0] and len(result[1]) != 0:
        for i in result[1]:
            home_data.append(list(i))
        for i in home_data:
            i[1] = str(i[1] + count)
        for i in range(6 - len(home_data)):
            home_data.append(['暂无课程', '0'])
    else:
        for i in range(6):
            home_data.append(['暂无课程', '0'])
    return home_data


# 获取课程数据
def get_course() -> tuple:
    db_common = models.Common()
    result = db_common.get_course()
    return result


# 获取学生已购买的课程数据
def get_stu_course(stu_name) -> list:
    db_student = models.student()
    result = db_student.get_stu_course(stu_name)
    stu_course = []
    if result[0] and result[1]:
        for i in result[1]:
            stu_course.append(i[0])
    return stu_course


# 购买课程
def purchase_courses(course_name, stu_name) -> bool:
    db_student = models.student()
    result = db_student.purchase_courses(course_name, stu_name)
    return result


# 退课
def drop_course(course_name, stu_name) -> bool:
    db_common = models.Common()
    result = db_common.stu_drop_course(course_name, stu_name)
    return result


# 获取学生课程数据
def get_my_course(username) -> tuple:
    db_student = models.student()
    db_common = models.Common()
    my_course_data = []
    result1 = db_student.get_my_course(username)
    if result1[0] and result1[1]:
        for i in result1[1]:
            tmp = db_common.count_class(i[0])
            my_course_data.append([*i, tmp])
        return True, my_course_data
    else:
        return False, '失败！'

# 加载欢迎语
def show_welcome_message():
    db_common = models.Common()
    result = db_common.get_welcome_message()
    return result

if __name__ == '__main__':
    get_my_course('谢帝')
