import ast
from enum import Enum, auto
from PIL import Image as PILImage
import pandas as pd

from utils.logger import LOG


# 定义内容类型
class ContentType(Enum):
    TEXT = auto()
    TABLE = auto()
    IMAGE = auto()

# 定义内容类
class Content:
    def __init__(self,content_type,original,translation=None):
        self.content_type = content_type # 内容类型
        self.original = original # 原文
        self.translation = translation # 译文
        self.status = False # 是否翻译过

    # 检查内容类型
    def check_translation_type(self,translation):
        if self.content_type == ContentType.TEXT and isinstance(translation,str):
            return True
        elif self.content_type == ContentType.TABLE and isinstance(translation,list):
            return True
        elif self.content_type == ContentType.IMAGE and isinstance(translation,PILImage.Image):
            return True
        return False

    # 将译文保存到 Content对象中
    def set_translation(self,translation,status):
        if not self.check_translation_type(translation):
            raise ValueError(f"Invalid translation type.Expected {self.content_type},but got{type(translation)}")
        self.translation = translation
        self.status = status

# 定义一个 表格的内容类，通过 pandas来处理表格内容
class TableContent(Content):
    def __init__(self,data,translation=None):
        # 使用 DataFrame来保存表格原文
        df = pd.DataFrame(data)

        # 校验行数、列数是否对得上
        if len(data) != len(df) or len(data[0]) != len(df.columns):
            raise ValueError("The number of rows and columns in the extracted table data and DataFrame object do not match.")
        super().__init__(ContentType.TABLE,df)

    def __str__(self):
        return self.original.to_string(header=False,index=False)

    def get_original_as_str(self):
        return self.original.to_string(header=False, index=False)

    # 定义惰性遍历方法
    def iter_items(self,translated = False):
        target_df = self.translation if translated else self.original
        for row_idx,row in target_df.iterrows():
            for col_idx,item in enumerate(row):
                yield(row_idx,col_idx,item)

    # 更新表格中的某项数据
    def update_item(self,row_idx,col_idx,new_value,translated=False):
        target_df = self.translation if translated else self.original
        target_df.at[row_idx,col_idx] = new_value


    def set_translation(self, translation, status):
        try:
            if not isinstance(translation, str):
                raise ValueError(f"Invalid translation type. Expected str, but got {type(translation)}")

            LOG.debug(f"[translation]\n{translation}")
            # 将 translation 转换为 列表类型
            translation_list = ast.literal_eval(translation)
            # Extract column names from the first set of brackets
            header = translation_list[0]
            # Extract data rows from the remaining brackets
            data_rows = translation_list[1:]
            # Replace Chinese punctuation and split each row into a list of values
            # Create a DataFrame using the extracted header and data
            translated_df = pd.DataFrame(data_rows, columns=header)
            LOG.debug(f"[translated_df]\n{translated_df}")
            self.translation = translated_df
            self.status = status
        except Exception as e:
            LOG.error(f"An error occurred during table translation: {e}")
            self.translation = None
            self.status = False

