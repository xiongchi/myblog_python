# -*- coding: utf-8 -*-

import os
import sys
import configparser
import logging.config

basedir = os.path.abspath(os.path.dirname(__file__))
config_file_name = 'config.ini'

logging.config.fileConfig("log.ini")
logger = logging.getLogger("simpleExample")


class Config:

    @staticmethod
    def get_conf():
        # exe_running_path = os.path.dirname(sys.executable)  # 获取exe所在路径
        exe_path = os.path.dirname(sys.path[0])  # 获取的是exe所在路径的上级路径
        if os.path.exists(os.path.join(exe_path, config_file_name)):
            file_path = os.path.join(exe_path, config_file_name)
        elif os.path.exists(config_file_name):
            file_path = config_file_name
        else:
            raise Exception('配置文件错误')
        config_parser = configparser.ConfigParser()
        config_parser.read(file_path)
        return config_parser

    # 公用配置
    @staticmethod
    def init_app(app):
        pass
    pass


# 测试配置
class DevelopConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/stock?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    pass


class ProductConfig(Config):
    #生产配置
    pass


config = {
    'development': DevelopConfig,
    'production': ProductConfig
}

