from typing import Optional


from book.content import ContentType
from translator.pdf_parser import PDFParser
from translator.translation_chain import TranslationChain
from translator.writer import Writer
from utils.logger import LOG


class PDFTranslator:
    def __init__(self,model_name:str):
        self.translation_chain = TranslationChain(model_name=model_name)
        self.pdf_parser = PDFParser()
        self.writer = Writer()

    # 翻译方法
    def translate_pdf(self,
                      input_file:Optional[str]=None,
                      output_file_format:str = "markdown",
                      source_language:str='English',
                      target_language:str = 'Chinese',
                      chinese_style=None,
                      pages:Optional[int] = 3): # 最多翻译三页，以免token消耗过多

        # 原pdf解析
        self.book = self.pdf_parser.parse_pdf(input_file=input_file, handle_pages=pages,target_language=target_language)

        for page_idx,page in enumerate(self.book.pages):
            for content_idx,content in enumerate(page.contents):
                # 调用 LLM 进行翻译获取译文
                translation,status = self.translation_chain.invoke(
                    inputs=content,
                    source_language=source_language,
                    target_language=target_language,
                    chinese_style=chinese_style
                )
                LOG.info(f"[translated text] {translation}")
                self.book.pages[page_idx].contents[content_idx].set_translation(translation,status)
        # 将译文进行保存
        return self.writer.save_translated_book(self.book, output_file_format=output_file_format)





