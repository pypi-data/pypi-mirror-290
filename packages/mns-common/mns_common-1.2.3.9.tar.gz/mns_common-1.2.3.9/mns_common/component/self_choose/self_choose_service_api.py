import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 16
project_path = file_path[0:end]
sys.path.append(project_path)
from mns_common.db.MongodbUtil import MongodbUtil

mongodb_util = MongodbUtil('27017')
import mns_common.constant.db_name_constant as db_name_constant
from functools import lru_cache


# 获取自选板块信息
@lru_cache(maxsize=None)
def get_self_choose_plate_list():
    return mongodb_util.find_all_data(db_name_constant.SELF_CHOOSE_PLATE)


# 获取自选股票
@lru_cache()
def get_self_choose_stocks():
    self_choose_stocks_df = mongodb_util.find_all_data(db_name_constant.SELF_CHOOSE_STOCK)
    return self_choose_stocks_df


# 清除缓存
def clear_self_choose_cache():
    get_self_choose_stocks.cache_clear()
    get_self_choose_plate_list.cache_clear()
