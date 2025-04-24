from book.content import Content


# 定义 页类型
class Page:
    def __init__(self):
        self.contents = [] # 一页里面有多个内容
    # 为页对象添加内容
    def add_content(self,content:Content):
        self.contents.append(content)
