"""
公共的数据库方法

"""
from conf import settings
from pymysql import Connection
import logging

#  导入日志
db_logger = logging.getLogger('db_数据库操作')


# 数据库连接
def conn_db():
    port, host, password, database, user = settings.db_setting()
    try:
        db = Connection(host=host, port=eval(port), passwd=password, user=user)
        cursor = db.cursor()
        db.select_db(database)
        db_logger.info('数据库连接成功')
        return cursor, db
    except Exception as e:
        db_logger.error('数据库连接失败', {e})
        return False


# 登陆查询
def login(username, password) -> tuple:
    cursor, db = conn_db()
    cursor.execute("SELECT * FROM Users WHERE username=%s AND password=%s;", (username, password))
    result = cursor.fetchall()
    if result == ():
        cursor.close()
        db.close()
        return False, ''
    cursor.close()
    db.close()
    # ->(name,角色，状态)
    return (result[0][1], result[0][3], result[0][4])


# 用户查询是否存在
def user_exist(username) -> bool:
    cursor, db = conn_db()
    cursor.execute("SELECT * FROM Users WHERE username=%s;", (username,))
    result = cursor.fetchall()
    if result == ():
        cursor.close()
        db.close()
        return False
    cursor.close()
    db.close()
    return True


# 删除用户
def db_delete(username) -> bool:
    cursor, db = conn_db()
    try:
        cursor.execute("DELETE FROM Users WHERE username=%s;", (username,))
        db.commit()  # 提交事务
        cursor.close()
        db.close()
        return True
    except Exception as e:
        # 发生异常时，回滚事务
        cursor.rollback()
        db_logger.info(f"删除失败: {e}")
        return False


# 冻结用户
def db_edit(username, state) -> bool:
    cursor, db = conn_db()
    try:
        cursor.execute("UPDATE Users SET state = %s WHERE username = %s;", (state, username,))
        db.commit()  # 提交事务
        cursor.close()
        db.close()
        return True
    except Exception as e:
        # 发生异常时，回滚事务
        cursor.rollback()
        db_logger.info(f"冻结用户失败: {e}")
        return False


# 课程数据
def db_get_course() -> tuple:
    cursor, db = conn_db()
    query = """
    SELECT
    c.course_name AS '课程名',
    c.price AS '课程价格',
    COUNT(scp.student_id) AS '购买人数',
    u.username AS '任课教师用户名',
    c.created_at AS '课程创建时间'
FROM
    Courses c
JOIN Teachers t ON c.class_teacher_id = t.teacher_id
JOIN Users u ON t.user_id = u.user_id
LEFT JOIN StudentCoursePurchase scp ON c.course_id = scp.course_id
GROUP BY
    c.course_id, c.course_name, c.price,u.username, c.created_at
ORDER BY
    c.created_at DESC; 
    """
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        db.close()
        return True, result
    except Exception as e:
        db_logger.info(f"获取课程数据失败: {e}")
        return False, '数据错误'


# 获取虚拟学习人数
def db_get_quantity() -> int:
    cursor, db = conn_db()
    try:
        cursor.execute("SELECT count FROM Learning_quantity WHERE setting_id=1;")
        result = cursor.fetchone()
        cursor.close()
        db.close()
        return result[0]
    except Exception as e:
        db_logger.info(f"获取虚拟人数失败: {e}")
        return False


# 学生退课
def db_stu_drop_course(course_name, stu_name) -> bool:
    cursor, db = conn_db()
    try:
        query = """SELECT C.course_id ,  U.user_id FROM Users U JOIN StudentCoursePurchase SCP on U.user_id = SCP.student_id
        JOIN Courses C on C.course_id = SCP.course_id
        WHERE C.course_name=%s AND U.username = %s; 
        """
        query2 = "DELETE FROM StudentCoursePurchase WHERE course_id=%s AND student_id=%s;"
        cursor.execute(query, (course_name, stu_name))
        result = cursor.fetchone()
        cursor.execute(query2, result)
        db.commit()
        cursor.close()
        db.close()
        return True
    except Exception as e:
        # 发生异常时，回滚事务
        cursor.rollback()
        db_logger.info(f"退课失败: {e}")
        return False


# 查询指定班级人数
def db_count_class(course_name) -> tuple:
    cursor, db = conn_db()
    try:
        query = """SELECT COUNT(course_name) FROM Courses C
                JOIN StudentCoursePurchase SCP on C.course_id = SCP.course_id
                WHERE course_name=%s;"""
        cursor.execute(query, course_name)
        result = cursor.fetchone()
        cursor.close()
        db.close()
        return result[0]
    except Exception as e:
        db_logger.info(f"获取虚拟人数失败: {e}")


# 获取首页数据
def db_get_home_data() -> tuple:
    cursor, db = conn_db()
    try:
        query = """
                SELECT
                C.course_name,
                COUNT(SCP.student_id) AS course_students_count
            FROM
                Courses C
            LEFT JOIN
                StudentCoursePurchase SCP ON C.course_id = SCP.course_id
            GROUP BY
                C.course_name
            ORDER BY
                course_students_count DESC
            LIMIT 6;
                """
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        db.close()
        return True, result
    except Exception as e:
        db_logger.error("出现错误", e)
        return False, '查询出错！'


def db_get_welcome_message()->tuple:
    cursor, db = conn_db()
    try:
        query = "SELECT message_content FROM Content WHERE id = 1 "
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        db.close()
        return True, result[0]
    except Exception as e:
        db_logger.error("出现错误", e)
        return False, '查询出错！'
