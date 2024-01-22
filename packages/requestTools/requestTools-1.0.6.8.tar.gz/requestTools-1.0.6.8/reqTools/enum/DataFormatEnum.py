# -*- coding:utf-8 -*-

from enum import Enum
import csv
import json
from io import StringIO

class DataFormatEnum(Enum):
    """数据格式枚举类
    """

    CSV = 'CSV'

    JSON = 'JSON'

    def __init__(self, formatName):
        self.formatName = formatName


    def formatToJson(self,text_data):

        if self == DataFormatEnum.CSV:
            # 使用StringIO来模拟一个文件
            csv_file = StringIO(text_data)
            # 读取CSV数据
            csv_reader = csv.DictReader(csv_file)
            csv_data = [row for row in csv_reader]
            # 将CSV数据转换为JSON格式的字符串
            json_string = json.dumps(csv_data, indent=4)
            return json.loads(json_string)

        elif self == DataFormatEnum.JSON:
            return json.loads(text_data)
        else:
            return json.loads(text_data)

    @staticmethod
    def getEnum(formatName):
        """
        根据枚举字符变量，找到对应枚举实例
        :param text: 数据文本
        :return: 返回对应枚举实例
        """
        for name, dataFormatEnum in DataFormatEnum.__members__.items():
            if dataFormatEnum.formatName == formatName:
                return dataFormatEnum
