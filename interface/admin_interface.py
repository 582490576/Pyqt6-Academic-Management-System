"""
    管理员接口

"""
import re

from db import models
from lib import common


# 管理员数据预览
def data_preview() -> list:
    admin = models.Admin()
    # 对返回的数据进行处理
    result = list(admin.data_preview())
    if result[0]:
        for i in range(1, 7):
            if result[i] is None:
                result[i] = '0'
            result[i] = str(result[i])
    return result


# 学生信息页，获取数据处理
def get_data_stu(option) -> list:
    admin = models.Admin()
    """
    1 = 全部学生数据
    2 = 购买课程的学生数据
    3 = 未购买课程的学生数据
    :param option:
    :return: list
    """
    result = admin.stu_data()
    if not result[0]:
        return list(result)
    result = common.state_user(result, 2)
    if option == 1:
        return result
    elif option == 2:
        stu_paid_list = []
        for i in result:
            if i[1] > 0:
                stu_paid_list.append(i)
        if len(stu_paid_list) == 0:
            return [False, '空数据！']
        return stu_paid_list
    elif option == 3:
        stu_notpaid_list = []
        for i in result:
            if i[1] == 0:
                stu_notpaid_list.append(i)
        if len(stu_notpaid_list) == 0:
            return [False, '空数据！']
        return stu_notpaid_list


# 学生信息查询
def stu_query(text_query) -> list:
    admin = models.Admin()
    result = admin.stu_query(text_query)
    if not result[0]:
        return result
    result = common.state_user(result, 2)
    return result


# 删除学生
def delete_stu(username):
    db_common = models.Common()
    db_common.user_delete(username)


# 冻结学生
def edit_stu(user_list):
    db_common = models.Common()
    if user_list[2] == '正常':
        state = '0'
    else:
        state = '1'
    db_common.user_edit(user_list[0], state)


# 获取课程数据
def get_course():
    db_common = models.Common()
    result = db_common.get_course()
    return result


# 创建课程
def add_course(name, price, teacher) -> tuple:
    if not re.match(r"^[-+]?[0-9]*\.?[0-9]+$", price):
        return False, '价格不符合规定！'
    if not float(price) >= 0:
        return False, '价格不符合规定！'
    if re.match(r'^[\u4e00-\u9fa5a-zA-Z0-9]{2,8}$', teacher) is None:
        return False, '任课教师不存在！'
    db_admin = models.Admin()
    result = db_admin.add_course(name, float(price), teacher)
    return result


# 注册教师
def add_teacher(username, password, salary) -> tuple:
    db_admin = models.Admin()
    db_common = models.Common()
    username = username.strip()
    password = password.strip()
    salary = salary.strip()
    # 校验账号密码薪资
    if re.match(r'^[\u4e00-\u9fa5a-zA-Z0-9]{2,8}$', username) is None:
        return False, '账号不符合规定！'
    if re.match(r'^[0-9a-zA-Z]{6,8}$', password) is None:
        return False, '密码不符合规定！'
    if re.match(r"^[-+]?[0-9]*\.?[0-9]+$", salary) and float(salary) >= 0:
        salary = float(salary)
    else:
        return False, '薪资不符合规定！'
    # 用户查重
    if db_common.user_exist(username):
        return False, '用户名已存在！'
    # 加密
    password = common.pw_to_sha512(password)

    # 写入数据库
    result = db_admin.add_teacher(username, password, salary)
    if not result:
        return False, '注册失败！'
    return True, '注册成功！'


# 获取教师数据
def get_teacher_data(_op=0) -> tuple:
    """
    获取教师数据
    :param _op: 0为全部教师数据，1为工资页教师数据
    :return:
    """
    db_admin = models.Admin()
    result = db_admin.get_teacher_data()
    if not result[0]:
        return False, '数据为空！'
    result = common.state_user(result, 3)
    if _op == 1:
        for i in result:
            del i[1]
            del i[3]
        return True, result
    else:
        return True, result


# 修改教师信息
def change_teacher(user_data, salary, is_state) -> tuple:
    db_admin = models.Admin()
    if user_data[2] != salary:
        if not re.match(r"^[-+]?[0-9]*\.?[0-9]+$", salary):
            return False, '薪资不符合规定！'
        if not float(salary) >= 0:
            return False, '薪资不符合规定！'
    result1 = db_admin.change_teacher_salary(user_data[0], float(salary))
    if not result1:
        return False, '修改失败！'
    if is_state:
        if user_data[3] == '正常':
            state = '0'
        else:
            state = '1'
        result2 = db_admin.change_teacher_stata(user_data[0], state)
        if not result2:
            return False, '修改失败！'
    return True, '修改成功！'


# 删除课程
def delete_course(course_data):
    db_admin = models.Admin()
    db_admin.delete_course(course_data)


# 编辑课程
def edite_course(user_data, course_name, course_price, course_teacher) -> tuple:
    if user_data[1] != course_price:
        if not re.match(r"^[-+]?[0-9]*\.?[0-9]+$", course_price):
            return False, '价格不符合规定！'
        if not float(course_price) >= 0:
            return False, '价格不符合规定！'
    if user_data[3] != course_teacher:
        if re.match(r'^[\u4e00-\u9fa5a-zA-Z0-9]{2,8}$', course_teacher) is None:
            return False, '任课教师不存在！'
    db_admin = models.Admin()
    return db_admin.edite_course(user_data[0], course_name, float(course_price), course_teacher)


# 发工资
def get_paid(user_data) -> tuple:
    db_admin = models.Admin()
    result = db_admin.get_paid(user_data)
    return result


# 流水
def get_flow_data() -> tuple:
    db_admin = models.Admin()
    result = db_admin.get_flow_data()
    return result


# 欢迎语
def save_welcome(text):
    db_admin = models.Admin()
    result = db_admin.save_welcome(text)
    return result


# 虚拟人数
def save_ai(count) -> tuple:
    db_admin = models.Admin()
    if re.match(r'^[1-9][0-9]*$', count):
        result = db_admin.save_ai(count)
    else:
        return False, '虚拟人数不合法！'
    if not result:
        return False, '数据库出错！'
    return True, '保存成功！'
