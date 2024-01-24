import numpy as np
import pandas as pd

from featureuitls import typeUtils

info_flag = "[ALIOTH - INFO - FEATURE_NAME] "  # <feature>为占位符
error_flag = "[ALIOTH - ERROR] "


def print_error_info(info_type):
    if info_type == "table_name":
        print(error_flag + "wrong table_name type, please use string")
    elif info_type == "data":
        print(error_flag + "wrong data type, please check your data type")


def print_info(data, table_name):
    print(info_flag)
    print("[" + ",".join(data) + "]")
    print(table_name)


def get_feature_info(data, table_name=""):
    """
    获取特征信息: 读取第一行/表头并输出
    :param data: 数组、字典、dataFrame、numpy.array、csv、excel（表格使用路径传入）
    :param table_name: 表名
    :return: 输出信息至控制台
    """
    # 判断格式
    table_name_type = typeUtils.get_data_type(table_name)
    if table_name_type != "string":
        print_error_info("table_name")
        return
    data_type = typeUtils.get_data_type(data)
    if data_type == "other":
        print_error_info("data")
        return
    else:
        # 一维数组直接输出
        try:
            if data_type == "list" and len(np.array(data).shape) == 1:
                print_info(list(map(str, data)), table_name)
                return
        except Exception as e:
            print_error_info("data")
            return
        # 其他
        try:
            # 格式转换
            df_data = typeUtils.change_type_to_dataframe(data, data_type)
        except Exception as e:
            print_error_info("data")
            return
        if df_data.empty:
            print_error_info("data")
            return
    print_info(df_data.columns, table_name)
