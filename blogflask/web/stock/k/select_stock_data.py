#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
from web import db


class SelectStockData(object):
    def __init__(self):
        self.db_engine = db.engine

    # common查询
    def common_select(self, sql):
        results = None
        try:
            results = self.db_engine.execute(sql).fetchall()
        except:
            print("Error: unable to fetch data")
        return results

    # 股票信息
    def sel_stock_code(self):
        sql = "select code, name, c_name  from stock_code_name"
        codes = np.array(self.common_select(sql))
        return codes[:, 0]

    def sel_k_day_secucode(self):
        sql = "select t.secucode from k_day t"
        k_day_data = np.array(self.common_select(sql))
        return k_day_data[:, 0]

    def sel_k_by_code(self, secucode, days):
        sql = "select * from k_day t where t.secucode = " + secucode + " order by t.date desc limit " + str(days)
        k_data = np.array(self.common_select(sql))
        return k_data[::-1]

    def sel_secuname(self, secucode):
        sql = "select name from stock_code_name where code= " + secucode
        name = self.common_select(sql)
        return str(name[0][0])



