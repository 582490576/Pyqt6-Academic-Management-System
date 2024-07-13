drop database AAMS;
create database AAMS;
use AAMS;


# 用户表   role角色 1 学生 2 教师 3 管理员 state 0冻结 1正常
-- 创建用户表
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('1', '2', '3') NOT NULL,
    state  ENUM('0','1') NOT NULL DEFAULT '1',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- 添加的列，自动记录插入时间
);



-- 创建老师表
CREATE TABLE Teachers (
    teacher_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL ,
    telephone VARCHAR(255) default '未设置',
    salary FLOAT NOT NULL ,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- 创建课程表
CREATE TABLE Courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    class_teacher_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 添加的列，自动记录插入时间
    FOREIGN KEY (class_teacher_id) REFERENCES Teachers(teacher_id) ON DELETE CASCADE
);

-- 创建流水表
CREATE TABLE Flow (
    flow_id INT AUTO_INCREMENT PRIMARY KEY,
    flow_name varchar(64) NOT NULL,
    money varchar(64) NOT NULL ,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    type ENUM('收入', '支出') NOT NULL
);

-- 创建设置表
CREATE TABLE  Learning_quantity (
    setting_id INT AUTO_INCREMENT PRIMARY KEY,
    count INT NOT NULL     -- 虚拟学习人数
);

CREATE TABLE Content(
    id INT AUTO_INCREMENT PRIMARY KEY,
    message_content TEXT NOT NULL   -- 主页欢迎语
);



-- 创建学生购买课程表
CREATE TABLE StudentCoursePurchase (
    purchase_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    course_id INT,
    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP , -- 购买日期
    FOREIGN KEY (student_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON DELETE CASCADE
);







# 密码123456进行了加密
insert into Users(username, password, role,state) value ('admin' ,'bbd606727010e81efdabca3160a851fe3b7d0ce5df620e3df651537744c7cbf9fc55aabe79644864d1d7fbfb11dc0c1ae8173787b2865e4e6433144451575620','3','1');

insert into Users(username, password, role,state) value ('大' ,'bbd606727010e81efdabca3160a851fe3b7d0ce5df620e3df651537744c7cbf9fc55aabe79644864d1d7fbfb11dc0c1ae8173787b2865e4e6433144451575620','1','1');
insert into Users(username, password, role,state) value ('小' ,'bbd606727010e81efdabca3160a851fe3b7d0ce5df620e3df651537744c7cbf9fc55aabe79644864d1d7fbfb11dc0c1ae8173787b2865e4e6433144451575620','1','1');
insert into Users(username, password, role,state) value ('1' ,'bbd606727010e81efdabca3160a851fe3b7d0ce5df620e3df651537744c7cbf9fc55aabe79644864d1d7fbfb11dc0c1ae8173787b2865e4e6433144451575620','1','1');
insert into Users(username, password, role,state) value ('2' ,'bbd606727010e81efdabca3160a851fe3b7d0ce5df620e3df651537744c7cbf9fc55aabe79644864d1d7fbfb11dc0c1ae8173787b2865e4e6433144451575620','1','1');
insert into Users(username, password, role,state) value ('3' ,'bbd606727010e81efdabca3160a851fe3b7d0ce5df620e3df651537744c7cbf9fc55aabe79644864d1d7fbfb11dc0c1ae8173787b2865e4e6433144451575620','1','1');
insert into Users(username, password, role,state) value ('4' ,'bbd606727010e81efdabca3160a851fe3b7d0ce5df620e3df651537744c7cbf9fc55aabe79644864d1d7fbfb11dc0c1ae8173787b2865e4e6433144451575620','1','1');
insert into Users(username, password, role,state) value ('5' ,'bbd606727010e81efdabca3160a851fe3b7d0ce5df620e3df651537744c7cbf9fc55aabe79644864d1d7fbfb11dc0c1ae8173787b2865e4e6433144451575620','1','1');
insert into Users(username, password, role,state) value ('6' ,'bbd606727010e81efdabca3160a851fe3b7d0ce5df620e3df651537744c7cbf9fc55aabe79644864d1d7fbfb11dc0c1ae8173787b2865e4e6433144451575620','1','1');
insert into Content(message_content) value ('欢迎来到FGG的教务管理系统！');
insert into Learning_quantity(count) value (0);