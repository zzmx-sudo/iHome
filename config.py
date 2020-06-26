# coding:utf-8

import redis

class Config(object):
    """配置信息"""
    SECRET_KEY = 'adaosfk1203rsdmdkfh3*rsfsg'

    # 数据库
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@127.0.0.1:3306/ihome'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # redis
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    # flask_session配置
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True  # 对cookie中的session_id进行隐藏
    PERMANENT_SESSION_LIFETIME = 86400  # session数据的有效期，单位：秒

class DevelopmentConfig(Config):
    """开发环境的配置信息"""
    DEBUG = True

class ProductionConfig(Config):
    """生产环境的配置信息"""
    pass

config_dict_map = {
    'develop':DevelopmentConfig,
    'product':ProductionConfig
}