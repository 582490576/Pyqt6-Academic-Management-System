"""

    配置文件

"""
import configparser
import os.path
import logging.config

# 项目根目录
BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)



# 获取数据库的配置文件
def db_setting():
    config = configparser.ConfigParser()
    # 获取路径
    config.read(f"{BASE_DIR}/conf.ini", encoding="UTF-8")
    host = config.get('MYSQL', 'host')
    port = config.get('MYSQL', 'port')
    password = config.get('MYSQL', 'password')
    db = config.get('MYSQL', 'db')
    user = config.get('MYSQL', 'user')
    return port, host, password, db, user


# 日志配置字典
LOGGING_DIC = {
    'version': 1.0,
    'disable_existing_loggers': False,
    # 日志格式
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(threadName)s:%(thread)d [%(name)s] %(levelname)s [%(pathname)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '%(asctime)s [%(name)s] %(levelname)s  %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'test': {
            'format': '%(asctime)s %(message)s',
        },
    },
    'filters': {},
    # 日志处理器
    'handlers': {
        'console_debug_handler': {
            'level': 'DEBUG',  # 日志处理的级别限制
            'class': 'logging.StreamHandler',  # 输出到终端
            'formatter': 'simple'  # 日志格式
        },
        'file_info_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件,日志轮转
            'filename': os.path.join(BASE_DIR, 'log', 'user.log'),
            'maxBytes': 1024 * 1024 * 10,  # 日志大小 10M
            'backupCount': 10,  # 日志文件保存数量限制
            'encoding': 'utf-8',
            'formatter': 'standard',
        },

    },
    # 日志记录器
    'loggers': {
        '': {  # 导入时logging.getLogger时使用的app_name
            'handlers': ['console_debug_handler', 'file_info_handler'],  # 日志分配到哪个handlers中
            'level': 'DEBUG',  # 日志记录的级别限制
            'propagate': False,  # 默认为True，向上（更高级别的logger）传递，设置为False即可，否则会一份日志向上层层传递
        },
    }
}

# 导入字典
logging.config.dictConfig(LOGGING_DIC)
