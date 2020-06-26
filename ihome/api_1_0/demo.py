# coding:utf-8

from . import api
from ihome import models

@api.route('/')
def index():
    return 'index page'
