from book.page import Page


# 定义 书对象
class Book:
    def __init__(self,pdf_file_path,target_language):
        self.pdf_file_path = pdf_file_path
        self.target_language = target_language
        self.pages = []


    # 为书对象添加页对象
    def add_page(self,page:Page):
        self.pages.append(page)