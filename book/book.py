from book.page import Page


# 定义 书对象
class Book:
    def __init__(self,pdf_file_path):
        self.pdf_file_path = pdf_file_path
        self.pages = []

    # 为书对象添加页对象
    def add_page(self,page:Page):
        self.pages.append(page)