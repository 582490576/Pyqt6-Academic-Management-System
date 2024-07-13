"""
学生类

"""

from conf import settings
import logging

from db.db_handler.db_common import conn_db

#  导入日志
db_logger = logging.getLogger('db_数据库操作')


class DbStudent(object):
    def __init__(self):
        self.cursor, self.db = conn_db()

    def __del__(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.db is not None:
            self.db.close()

    # 注册
    def db_register(self, username, password) -> bool:
        try:
            self.cursor.execute("INSERT INTO Users(username, password, role) VALUES(%s,%s,%s)", (username, password, 1))
            self.db.commit()
            return True
        except Exception as e:
            self.cursor.rollback()
            db_logger.error("学生注册出现错误", e)
            return False



    # 获取学生已购买的课程数据
    def db_get_stu_course(self, stu_name) -> tuple:
        try:
            query1 = 'SELECT user_id FROM Users WHERE username =%s ;'
            query2 = """SELECT c.course_name FROM Courses c 
                        LEFT JOIN StudentCoursePurchase s 
                        ON s.course_id = c.course_id 
                        WHERE student_id =%s ;
                        """
            self.cursor.execute(query1, stu_name)
            stu_id = self.cursor.fetchone()
            self.cursor.execute(query2, stu_id)
            result = self.cursor.fetchall()
            return True, result
        except Exception as e:
            db_logger.error("获取数据出现错误", e)
            return False, '查询出错！'

    # 购买课程
    def db_purchase_courses(self, course_name, stu_name) -> bool:
        try:
            query1 = 'SELECT user_id FROM Users WHERE username =%s ;'
            query2 = "SELECT course_id,price FROM Courses WHERE course_name =%s;"
            query3 = "INSERT INTO StudentCoursePurchase(student_id,course_id) VALUES (%s,%s);"
            query4 = "INSERT INTO Flow(flow_name,money,type) VALUES (%s,%s,'收入');"
            self.cursor.execute(query1, stu_name)
            stu_id = self.cursor.fetchone()[0]
            self.cursor.execute(query2, course_name)
            course_id = self.cursor.fetchone()
            self.cursor.execute(query3, (stu_id, course_id[0]))
            self.cursor.execute(query4, (course_name, course_id[1]))
            self.db.commit()
            return True
        except Exception as e:
            self.cursor.rollback()
            db_logger.error("出现错误", e)
            return False

    # 获取我的课程数据
    def db_get_my_course(self, course_name)->tuple:
        try:
            query1 = """
                SELECT C.course_name,U2.username,T.telephone FROM Users U
                LEFT JOIN StudentCoursePurchase S on U.user_id = S.student_id
                LEFT JOIN Courses C on C.course_id = S.course_id
                LEFT JOIN Teachers T on C.class_teacher_id = T.teacher_id
                LEFT JOIN Users U2 on U2.user_id = T.user_id
                WHERE U.username = %s;
            """

            self.cursor.execute(query1, course_name)
            course_data = self.cursor.fetchall()
            return True,course_data
        except Exception as e:
            db_logger.error("出现错误", e)
            return False,'出现错误'


if __name__ == '__main__':
    a = DbStudent()
    print(a.db_get_my_course('谢帝'))
