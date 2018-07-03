# coding:utf-8
from flask import Blueprint

stock = Blueprint('stock', __name__,)
from web.stock import views
