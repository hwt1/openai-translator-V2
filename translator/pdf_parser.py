from typing import Optional

import pdfplumber
from werkzeug.datastructures import FileStorage

from book.book import Book
from book.content import Content, ContentType, TableContent
from book.page import Page
from translator.exceptions import PageOutOfRangeException
from utils.logger import LOG


class PDFParser:
    # 解析pdf文件，将pdf文件封装成 book对象
    def parse_pdf(self,pdf_file_path:Optional[str]=None,pdf_file:Optional[FileStorage]=None,handle_pages:Optional[int] = None):
        book = Book(pdf_file_path)

        # 读取 pdf文件
        with pdfplumber.open(pdf_file_path if pdf_file_path else pdf_file) as pdf:
            if handle_pages is not None and handle_pages > len(pdf.pages):
                raise PageOutOfRangeException(len(pdf.pages),handle_pages)

            # 获取需要处理的 pdf中的 page对象
            if handle_pages is None:
                pages_to_parse = pdf.pages
            else:
                pages_to_parse = pdf.pages[:handle_pages]

            # 遍历处理 pdf中的每页内容
            for pdf_page in pages_to_parse:
                page = Page()
                # 获取单页pdf中不包括表格部分的文本
                raw_text = self.extract_text_without_table(pdf_page)

                # 获取表格数据
                tables = pdf_page.extract_tables()

                # 处理文本内容
                if raw_text:
                    raw_text_lines = raw_text.splitlines()
                    cleaned_raw_text_lines = [line.strip() for line in raw_text_lines if line.strip()]
                    cleaned_raw_text = "\n".join(cleaned_raw_text_lines)

                    text_content = Content(content_type=ContentType.TEXT,original=cleaned_raw_text)
                    page.add_content(text_content)
                    LOG.debug(f"[raw_text]\n {cleaned_raw_text}")

                # 处理表格数据
                if tables:
                    table = TableContent(tables)
                    page.add_content(table)
                    LOG.debug(f"[table]\n{table}")
                book.add_page(page)
        return book



    @staticmethod
    def extract_text_without_table(pdf_page):
        """ 提取指定单页不包含表格的文本内容 """
        # 获取页面中的表格区域
        table_areas = []
        for table in pdf_page.find_tables():
            table_areas.extend(table.bbox)

        pre_y=None
        # 排除表格区域的文本
        non_table_text = ""
        for char in pdf_page.chars:
            char_bbox = (char['x0'],char['top'],char['x1'],char['bottom'])
            is_in_table = False
            current_y = char['top']
            for i in range(0,len(table_areas),4):
                table_bbox = (table_areas[i],table_areas[i+1],table_areas[i+2],table_areas[i+3])
                if(char_bbox[0] >= table_bbox[0] and char_bbox[1] >= table_bbox[1]
                        and char_bbox[2] <= table_bbox[2] and char_bbox[3] <= table_bbox[3]):
                    is_in_table =True
                    break
            if not is_in_table:
                if pre_y is not None and current_y > pre_y:
                    non_table_text +='\n'
                non_table_text += char['text']
                pre_y = current_y
        return non_table_text


if __name__ =="__main__":
    pdf = PDFParser()
    pdf.parse_pdf("../tests/test.pdf")