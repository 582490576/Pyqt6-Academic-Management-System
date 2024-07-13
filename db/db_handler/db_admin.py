"""
    管理员数据库

"""

import logging
from db.db_handler.db_common import conn_db
from lib import common

#  导入日志
db_logger = logging.getLogger('db_数据库操作')


class DbAdmin(object):
    def __init__(self):
        self.cursor, self.db = conn_db()

    def __del__(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.db is not None:
            self.db.close()

    # 管理员数据预览
    def db_data_preview(self) -> tuple:
        total_students = None  # 累计付费人数
        today_revenue = None  # 今日营收
        accumulated_revenue = None  # 累计营收
        number_students = None  # 累计注册学生
        number_courses = None  # 课程数
        number_teachers = None  # 教师数
        try:
            self.cursor.execute("SELECT COUNT(DISTINCT student_id) FROM StudentCoursePurchase;")
            total_students = self.cursor.fetchone()[0]
            self.cursor.execute("SELECT money FROM Flow WHERE type = '收入' AND DATE(created_at) = CURDATE();")
            today_revenue = self.cursor.fetchall()
            self.cursor.execute("SELECT money FROM Flow WHERE type = '收入';")
            accumulated_revenue = self.cursor.fetchall()
            today_revenue = common.processing_flow(today_revenue)
            accumulated_revenue = common.processing_flow(accumulated_revenue)
            self.cursor.execute("SELECT COUNT(user_id) FROM Users WHERE role = '1';")
            number_students = self.cursor.fetchone()[0]
            self.cursor.execute("SELECT COUNT(course_id) FROM Courses ")
            number_courses = self.cursor.fetchone()[0]
            self.cursor.execute("SELECT COUNT(teacher_id) FROM Teachers ")
            number_teachers = self.cursor.fetchone()[0]
            return (
                True, total_students, today_revenue, accumulated_revenue, number_students, number_courses,
                number_teachers)
        except Exception as e:
            db_logger.error("数据查询出现错误！", e)
            return False, '数据查询出现错误！'

    # 学生数据页
    def db_stu_data(self) -> tuple:
        stu_data_all = None  # 所有学生数据
        query = """SELECT U.username,COUNT(SCP.purchase_id),U.state ,U.created_at 
                           FROM Users as U LEFT JOIN StudentCoursePurchase as SCP 
                           ON U.user_id = SCP.student_id WHERE U.role = '1' 
                           GROUP BY U.user_id ORDER BY U.user_id;"""
        try:
            self.cursor.execute(query)
            stu_data_all = self.cursor.fetchall()
            if not stu_data_all:
                return False, '数据为空！'
            return stu_data_all
        except Exception as e:
            db_logger.error("数据查询出现错误！", e)
            return False, '数据查询出现错误！'

    # 学生信息查询
    def db_stu_query(self, text_query) -> tuple:
        stu_data = None  # 查询数据
        query = """
        SELECT U.username, COUNT(SCP.purchase_id), U.state, U.created_at
        FROM Users as U
        LEFT JOIN StudentCoursePurchase as SCP
        ON U.user_id = SCP.student_id
        WHERE U.role = '1' AND U.username LIKE %s
        GROUP BY U.user_id
        ORDER BY U.user_id;
        """
        try:
            self.cursor.execute(query, ('%' + text_query + '%'))
            stu_data = self.cursor.fetchall()
            if not stu_data:
                return False, '数据为空！'
            return stu_data
        except Exception as e:
            db_logger.error("数据查询出现错误！", e)
            return False, '数据查询出现错误！'

    # 教师注册
    def db_add_teacher(self, username, password, salary) -> bool:
        try:
            # 使用变量传递角色ID，这里假设role_id是函数的参数或从其他地方获取
            query_user = "INSERT INTO Users(username, password, role, state) VALUES(%s, %s, '2', '1');"
            query_teacher = "INSERT INTO Teachers (user_id, salary) VALUES(%s, %s);"
            self.cursor.execute(query_user, (username, password))
            new_user_id = self.cursor.lastrowid
            self.cursor.execute(query_teacher, (new_user_id, salary))
            self.db.commit()
            return True
        except Exception as e:
            # 发生异常时，回滚事务，并记录详细的错误信息
            self.cursor.rollback()
            db_logger.info(f"添加教师失败: {str(e)}")
            return False

    # 获取教师数据
    def db_get_teacher_data(self):
        teacher_data = None  # 查询数据
        query = """
            SELECT 
                U.username ,
                COUNT(C.course_id) ,
                T.salary,
                U.state ,
                U.created_at
            FROM 
                Teachers T
            JOIN 
                Users U ON T.user_id = U.user_id
            LEFT JOIN 
                Courses C ON T.teacher_id = C.class_teacher_id
            GROUP BY 
                T.teacher_id, U.username, T.salary, U.state, U.created_at
            ORDER BY 
                T.teacher_id;
        """
        try:
            self.cursor.execute(query)
            teacher_data = self.cursor.fetchall()
            if not teacher_data:
                return False, '数据为空！'
            return teacher_data
        except Exception as e:
            db_logger.error("数据查询出现错误！", e)
            return False, '数据查询出现错误！'

    # 修改教师信息
    def db_change_teacher_salary(self, username, salary):
        try:
            get_id = "SELECT user_id FROM Users WHERE username=%s;"
            query = "UPDATE Teachers SET salary =%s WHERE user_id=%s;"
            self.cursor.execute(get_id, username)
            user_id = self.cursor.fetchall()
            self.cursor.execute(query, (salary, user_id))
            self.db.commit()
            return True
        except Exception as e:
            # 发生异常时，回滚事务，并记录详细的错误信息
            self.cursor.rollback()
            db_logger.error("数据查询出现错误！", e)
            return False

    def db_change_teacher_stata(self, username, state):
        try:
            query = "UPDATE Users SET state =%s WHERE username=%s;"
            self.cursor.execute(query, (state, username))
            self.db.commit()
            return True
        except Exception as e:
            # 发生异常时，回滚事务，并记录详细的错误信息
            self.cursor.rollback()
            db_logger.error("数据查询出现错误！", e)
            return False

    # 添加课程
    def db_add_course(self, course_name, price, teacher_name) -> tuple:
        try:
            # 获取教师ID
            query1 = "SELECT user_id FROM Users WHERE username=%s AND role = '2'; "
            self.cursor.execute(query1, teacher_name)
            user_id = self.cursor.fetchone()
            if not user_id:
                return False, '教师不存在！'
            query2 = "SELECT teacher_id FROM Teachers WHERE user_id=%s; "
            self.cursor.execute(query2, user_id)
            teacher_id = self.cursor.fetchone()

            # 课程名查重
            query3 = "SELECT * FROM Courses WHERE course_name=%s;"
            self.cursor.execute(query3, course_name)
            if self.cursor.fetchone():
                return False, '课程已存在！'
            # 写入数据
            query4 = "INSERT INTO Courses(course_name,price,class_teacher_id) VALUES (%s,%s,%s);"
            self.cursor.execute(query4, (course_name, price, teacher_id))
            self.db.commit()
            return True, '添加成功'
        except Exception as e:
            # 发生异常时，回滚事务，并记录详细的错误信息
            self.cursor.rollback()
            db_logger.error("数据查询出现错误！", e)
            return False

    # 删除课程
    def db_delete_course(self, course_data) -> bool:
        try:
            self.cursor.execute("DELETE FROM Courses WHERE course_name=%s;", (course_data,))
            self.db.commit()  # 提交事务
            return True
        except Exception as e:
            # 发生异常时，回滚事务
            self.cursor.rollback()
            db_logger.info(f"删除失败: {e}")
            return False

    # 编辑课程
    def db_edite_course(self, old_name, new_name, course_price, course_teacher) -> tuple:
        try:
            # 获取教师ID
            query1 = "SELECT user_id FROM Users WHERE username=%s AND role = '2'; "
            self.cursor.execute(query1, course_teacher)
            user_id = self.cursor.fetchone()
            if not user_id:
                return False, '教师不存在！'
            query2 = "SELECT teacher_id FROM Teachers WHERE user_id=%s; "
            self.cursor.execute(query2, user_id)
            teacher_id = self.cursor.fetchone()

            # 课程查重
            if old_name != new_name:
                query3 = "SELECT * FROM Courses WHERE course_name=%s;"
                self.cursor.execute(query3, new_name)
                if self.cursor.fetchone():
                    return False, '课程已存在！'
                query4 = "UPDATE Courses SET course_name =%s, price=%s,class_teacher_id=%s WHERE course_name=%s;"
                self.cursor.execute(query4, (new_name, course_price, teacher_id, old_name))
            else:
                query4 = "UPDATE Courses SET course_name =%s, price=%s,class_teacher_id=%s WHERE course_name=%s;"
                self.cursor.execute(query4, (new_name, course_price, teacher_id, old_name))
            self.db.commit()
            return True, '修改成功！'
        except Exception as e:
            # 发生异常时，回滚事务，并记录详细的错误信息
            self.cursor.rollback()
            db_logger.error("数据编辑出现错误！", e)

    # 发工资
    def db_get_paid(self, user_data) -> bool:
        try:
            self.cursor.execute("INSERT INTO  Flow(flow_name,money,type) VALUE(%s ,%s,'支出');",
                                (user_data[0], '-' + str(user_data[1])))
            self.db.commit()  # 提交事务
            return True
        except Exception as e:
            # 发生异常时，回滚事务
            self.cursor.rollback()
            db_logger.info(f"失败: {e}")
            return False

    # 流水
    def db_get_flow_data(self) -> tuple:
        try:
            self.cursor.execute("SELECT created_at,flow_name,money,type FROM Flow;")
            result = self.cursor.fetchall()
            return True, result
        except Exception as e:
            db_logger.info(f"查询失败: {e}")
            return False, '失败'

    # 保存欢迎语
    def db_save_welcome(self, text) -> bool:
        try:
            self.cursor.execute("UPDATE Content SET message_content =%s WHERE id=1;", text)
            self.db.commit()
            return True
        except Exception as e:
            db_logger.info(f"保存失败: {e}")
            return False

    # 保存虚拟人数
    def db_save_ai(self, count) -> bool:
        try:
            self.cursor.execute("UPDATE Learning_quantity SET count =%s WHERE setting_id=1;", count)
            self.db.commit()
            return True
        except Exception as e:
            self.cursor.rollback()
            db_logger.info(f"保存失败: {e}")
            return False


if __name__ == '__main__':
    Admin = DbAdmin()
    print(Admin.db_data_preview())
