import os.path
import sys

from translator.pdf_translator import PDFTranslator
from translator.translation_config import TranslationConfig
from utils.argument_parser import ArgumentParser

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ =='__main__':
    # 解析命令行
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()

    # 初始化配置单例
    config = TranslationConfig()
    config.initialize(args)

    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
    translator = PDFTranslator(model_name=config.model_name)
    translator.translate_pdf(input_file=config.input_file,output_file_format=config.output_file_format,pages=None)