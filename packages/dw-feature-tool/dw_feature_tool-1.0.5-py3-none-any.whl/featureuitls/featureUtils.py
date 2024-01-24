import numpy as np

from featureuitls import typeUtils

info_flag = "[ALIOTH - INFO - FEATURE_NAME] "  # <feature>为占位符
error_flag = "[ALIOTH - ERROR] "


def print_error_info(info_type):
    if info_type == "feature_name":
        print(error_flag + "wrong feature_name type, please input string or list")
    elif info_type == "data":
        print(error_flag + "wrong data type, please check your data type")


def print_info(data):
    print(info_flag)
    print("[" + ",".join(data) + "]")


def get_feature_info(data):
    """
    获取特征信息: 读取第一行/表头并输出
    :param data: 数组、字典、dataFrame、numpy.array、csv、excel（表格使用路径传入）
    :return: 输出信息至控制台
    """
    # 格式转换为DataFrame
    data_type = typeUtils.get_data_type(data)
    if data_type == "other":
        print_error_info("data")
        return
    else:
        # 一维数组直接输出
        if data_type == "list" and len(np.array(data).shape):
            print_info(data)
            return
        else:
            try:
                df_data = typeUtils.change_type_to_dataframe(data, data_type)
            except Exception as e:
                print_error_info("data")
                return
            if df_data.empty:
                print_error_info("data")
                return
    print_info(df_data.columns)

