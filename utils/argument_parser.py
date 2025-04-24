# 用于解析命令行参数
import argparse


class ArgumentParser:
    def __init__(self):
        # 创建 ArgumentParser 对象：该对象用于解析命令行参数。
        self.parser = argparse.ArgumentParser(description="Translate English PDF book to Chinese.")
        # 添加需要解析的参数
        self.parser.add_argument('--config',type=str,default='config.yaml',help='Configuration file about model and API settings.')
        # self.parser.add_argument('--model_type',type=str,required=True,choices=['GLMModel','OpenAIModel'],help='The type of transaction model to use. Choose between "GLMModel" and "OpenAIModel".')
        self.parser.add_argument('--glm_model_url', type=str, help='The URL of the ChatGLM model URL.')
        self.parser.add_argument('--timeout', type=int, help='Timeout for the API request in seconds.')
        self.parser.add_argument('--openai_model', type=str,help='The model name of OpenAI Model. Required if model_type is "OpenAIModel".')
        self.parser.add_argument('--openai_api_key', type=str,help='The API key for OpenAIModel. Required if model_type is "OpenAIModel".')
        self.parser.add_argument('--book', type=str, help='PDF file to translate.')
        self.parser.add_argument('--file_format', type=str, help='The file format of translated book. Now supporting PDF and Markdown')

    # 解析获取输入的命令行参数
    def parse_arguments(self):
        args = self.parser.parse_args()
        # if args.model_type == 'OpenAIModel' and not args.openai_model and not args.openai_api_key:
        #     self.parser.error("--openai_model and --openai_api_key is required when using OpenAIModel")
        return args

# 在 Terminal窗口 utils目录下执行命令：
# python .\argument_parser.py --model_type=OpenAIModel
# python .\argument_parser.py --help
if __name__ == '__main__':
    arg_parser = ArgumentParser()
    print(f"============{arg_parser.parse_arguments()},type:{type(arg_parser.parse_arguments())}") # <class 'argparse.Namespace'>