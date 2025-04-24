# 用于解析命令行参数
import argparse


class ArgumentParser:
    def __init__(self):
        # 创建 ArgumentParser 对象：该对象用于解析命令行参数。
        self.parser = argparse.ArgumentParser(description="A translation tool that supports translations in any language pair.")
        # 添加需要解析的参数
        self.parser.add_argument('--config_file', type=str, default='config.yaml',
                                 help='Configuration file with model and API settings.')
        self.parser.add_argument('--model_name', type=str, help='Name of the Large Language Model.')
        self.parser.add_argument('--input_file', type=str, help='PDF file to translate.')
        self.parser.add_argument('--output_file_format', type=str,
                                 help='The file format of translated book. Now supporting PDF and Markdown')
        self.parser.add_argument('--source_language', type=str,
                                 help='The language of the original book to be translated.')
        self.parser.add_argument('--target_language', type=str,
                                 help='The target language for translating the original book.')

    # 解析获取输入的命令行参数
    def parse_arguments(self):
        args = self.parser.parse_args()
        return args

# 在 Terminal窗口 utils目录下执行命令：
# python .\argument_parser.py --model_type=OpenAIModel
# python .\argument_parser.py --help
if __name__ == '__main__':
    arg_parser = ArgumentParser()
    print(f"============{arg_parser.parse_arguments()},type:{type(arg_parser.parse_arguments())}") # <class 'argparse.Namespace'>