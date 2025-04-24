import os
import sys

from model.openai_model import OpenAIModel
from translator.pdf_translator import PDFTranslator
from utils.argument_parser import ArgumentParser
from utils.config_loader import ConfigLoader

# 获取项目根路径的绝对路径
project_root =os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,project_root)

if __name__ == "__main__":
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()
    config_loader = ConfigLoader(args.config)

    config = config_loader.load_config()

    model_name = args.openai_model
    api_key = args.openai_api_key

    model = OpenAIModel(model='gpt-3.5-turbo',api_key=api_key)

    pdf_file_path = args.book if args.book else config['common']['book']
    file_format = args.file_format if args.file_format else config['common']['file_format']

    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
    translator = PDFTranslator(model)
    translator.translate_pdf(pdf_file_path)