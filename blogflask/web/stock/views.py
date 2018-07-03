import os

from flask import send_file

from web.stock import stock
from web.stock.k.k_photo import KPhoto
from config import Config


@stock.route('hello/<secucode>/<days>', methods=['GET', ])
def get_stock(secucode, days):
    path = Config.get_conf().get('photo', 'path')
    if secucode == '':
        return '请输入正确代码'
    if days == '':
        days = 50
    KPhoto(secucode, days).k_photo()
    return send_file(os.path.join(path, secucode + '_' + days + '.png'))