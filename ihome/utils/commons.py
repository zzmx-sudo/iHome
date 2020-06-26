# coding:utf-8

from werkzeug.routing import BaseConverter
from flask import jsonify,session,g
from ihome.utils.response_code import RET
import functools

# 定义正则转换器
class ReConverter(BaseConverter):
    """"""
    def __init__(self, url_map, regex):
        # 调用父类的初始化方法
        super(ReConverter,self).__init__(url_map)
        # 保存正则表达式
        self.regex = regex


# 定义验证登录状态装饰器
def login_required(view_func):

    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        # 判断用户的登录状态
        user_id = session.get("user_id")

        # 如果用户是登录的，直接执行视图函数
        if user_id is not None:
            # 应用上下文保存用户的id
            g.user_id = user_id
            return view_func(*args, **kwargs)
        # 如果未登录，返回未登录的信息
        else:
            return jsonify(errno=RET.SESSIONERR, errmsg='用户未登录')

    return wrapper
