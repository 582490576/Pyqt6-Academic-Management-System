"""
    公共方法
"""

import hashlib
import os


# 加密
def pw_to_sha512(password) -> hashlib:
    hash_sha512 = hashlib.sha512()
    hash_sha512.update(password.encode('utf-8'))
    hash_sha512.update("来自FGG的加密sha512".encode('utf-8'), )
    return hash_sha512.hexdigest()


# 状态识别
state = {
    '0': "冻结",
    '1': "正常"
}


def state_user(data_list, _op, is_list=None) -> list:
    """
        将数据列表中的状态码进行更换
    :param data_list: 处理的数据列表
    :param _op: 位置下标
    :param is_list: 数组类型None为元组，Ture为列表
    :return: list
    """
    if is_list is None:
        new_data_list = []
        for i in data_list:
            temp = list(i)
            temp[_op] = state[temp[_op]]
            new_data_list.append(temp)
        return new_data_list
    else:
        for i in data_list:
            i[_op] = state[i[_op]]
        return data_list


# 处理流水金额 元组
def processing_flow(tmp_tuple) -> float:
    count = 0
    if tmp_tuple:
        for i in tmp_tuple:
            count += float(i[0])
        return count
    return 0.00


# 获取imgs文件路径
def get_imgs_dirname():
    BASE_DIR = os.path.dirname(
        os.path.dirname(__file__)
    )
    return BASE_DIR


if __name__ == '__main__':
    pw = pw_to_sha512('123456')
    print(pw)
