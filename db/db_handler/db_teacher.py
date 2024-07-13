"""
教师类

"""

from conf import settings
import logging

from db.db_handler.db_common import conn_db

#  导入日志
db_logger = logging.getLogger('db_数据库操作')


class DbTeacher(object):
    def __init__(self):
        self.cursor, self.db = conn_db()

    def __del__(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.db is not None:
            self.db.close()

    # 获取教师课程数据
    def db_get_teacher_course(self, user_name) -> tuple:
        try:
            query1 = """
            SELECT C.course_name,C.price FROM Users U JOIN Teachers T on U.user_id = T.user_id
            JOIN Courses C on T.teacher_id = C.class_teacher_id
            WHERE U.username=%s
            ;"""
            self.cursor.execute(query1, user_name)
            course_data = self.cursor.fetchall()
            return True, course_data
        except Exception as e:
            db_logger.error("出现错误", e)
            return False, '出现错误'

    # 获取班级成员列表
    def db_get_class_member(self, course_name) -> tuple:
        try:
            query1 = """
                    SELECT U.username,U.state,COUNT(U.username) FROM Users U JOIN StudentCoursePurchase SCP ON U.user_id = SCP.student_id
                        LEFT JOIN Courses C on C.course_id = SCP.course_id
                        LEFT JOIN StudentCoursePurchase S on U.user_id = S.student_id
                        WHERE C.course_name = %s
                        GROUP BY U.username
                    ;"""
            self.cursor.execute(query1, course_name)
            course_data = self.cursor.fetchall()
            return True, course_data
        except Exception as e:
            db_logger.error("出现错误", e)
            return False, '出现错误'

    def db_save_number(self, teacher_name, number) -> bool:
        try:
            query1 = "SELECT user_id FROM Users WHERE username = %s;"
            query2 = "UPDATE Teachers SET telephone=%s WHERE user_id = %s;"
            self.cursor.execute(query1, teacher_name)
            teacher_id = self.cursor.fetchall()
            self.cursor.execute(query2,(number, teacher_id))
            self.db.commit()
            return True
        except Exception as e:
            self.cursor.rollback()
            db_logger.error("出现错误", e)
            return False
