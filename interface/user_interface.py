"""
公共接口

"""
from db import models
from lib import common


# 账号密码校验
def user_login(username, password) -> tuple:
    username = username.strip()
    password = password.strip()
    # 加密
    password = common.pw_to_sha512(password)
    # 创建数据库对象
    db = models.Common()
    # 判断用户是否存在
    if not db.user_exist(username):
        return False, '用户不存在'
    # 判断账号密码是否正确,正确返回用户信息
    result = db.login(username,password)
    if not result[0]:
        return False, '密码错误，请重试'
    if result[2] == '0':
        return False, '账户已被冻结'
    return result


