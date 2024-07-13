"""
教师接口

"""
from db import models
from lib import common
import re


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


# 获取教师课程数据
def get_teacher_course(user_name: str) -> tuple:
    db_common = models.Common()
    db_teacher = models.teacher()
    result = db_teacher.get_teacher_course(user_name)
    my_course_data = []
    if result[0] and len(result[1]) != 0:
        for i in result[1]:
            tmp = db_common.count_class(i[0])
            my_course_data.append([*i, tmp])
        return True, my_course_data
    else:
        return False, '失败！'


# 获取班级成员列表
def get_class_member(course_name: str) -> tuple:
    db_teacher = models.teacher()
    result = db_teacher.get_class_member(course_name)
    return result


# 退课
def drop_course(course_name, stu_name) -> bool:
    db_common = models.Common()
    result = db_common.stu_drop_course(course_name, stu_name)
    return result


# 保存联系方式
def save_number(teacher_name, number):
    db_teacher = models.teacher()
    result = db_teacher.save_number(teacher_name, number)
    return result


# 加载欢迎语
def show_welcome_message():
    db_common = models.Common()
    result = db_common.get_welcome_message()
    return result


if __name__ == '__main__':
    print(get_teacher_course('大黄'))
