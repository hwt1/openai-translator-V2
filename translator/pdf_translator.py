from typing import Optional

from werkzeug.datastructures import FileStorage

from book.content import ContentType
from model.model import Model
from translator.pdf_parser import PDFParser
from translator.writer import Writer
from utils.logger import LOG


class PDFTranslator:
    def __init__(self,model:Model):
        self.model = model
        self.pdf_parser = PDFParser()
        self.writer = Writer()

    # 翻译方法
    def translate_pdf(self,pdf_file_path:Optional[str]=None,pdf_file:Optional[FileStorage]=None,file_format:str = "PDF",target_language:str = '中文',output_file_path:str = None,pages:Optional[int] = None):
        if pdf_file_path is None and pdf_file is None:
            raise ValueError("pdf_file_path 和 pdf_file 必须一个有值")
        self.book = self.pdf_parser.parse_pdf(pdf_file_path=pdf_file_path,pdf_file=pdf_file, handle_pages=pages)

        for page_idx,page in enumerate(self.book.pages):
            for content_idx,content in enumerate(page.contents):
                prompt = self.model.translate_prompt(content,target_language)
                LOG.debug(prompt)
                translation,status = self.model.make_request(prompt)
                LOG.info(translation)
                self.book.pages[page_idx].contents[content_idx].set_translation(translation,status)

        self.writer.save_translated_book(self.book, output_file_path, file_format)
        return "success"




