import gradio as gr

from translator.pdf_translator import PDFTranslator
from translator.translation_config import TranslationConfig
from utils.argument_parser import ArgumentParser
from utils.logger import LOG

# 初始化方法
def initialize_translator():
    # 解析命令行
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()

    # 初始化配置单例
    config = TranslationConfig()
    config.initialize(args)
    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
    global Translator
    Translator = PDFTranslator(config.model_name)

# gradio界面方式
def translation(input_file,source_language,target_language,output_file_format):
    LOG.debug(f"[翻译任务]\n源文件: {input_file.name}\n源语言: {source_language}\n目标语言: {target_language}")
    output_file_path = Translator.translate_pdf(
        input_file=input_file,
        source_language=source_language,
        target_language=target_language,
        output_file_format=output_file_format
    )
    return output_file_path

# 1、定义 gradio界面
def launch_gradio():
    app = gr.Interface(
        fn=translation,
        title='OpenAI-Translator v2.0(PDF 电子书翻译工具)',
        inputs=[
            gr.File(label='上传PDF文件'),
            gr.Textbox(label='原语言（默认英文）',placeholder='English',value='English'),
            gr.Textbox(label='目标语言（默认中文）',placeholder='Chinese',value='Chinese'),
            gr.Radio(["markdown", "pdf"], value='markdown',label="导出文件类型", info="请选择译文的文件类型"),
        ],
        outputs=[
            gr.File(label='下载翻译文件')
        ],
        allow_flagging="never"
    )
    app.launch(share=True,server_name='127.0.0.1',server_port=5555)


if __name__ == "__main__":
    # 初始化 translator
    initialize_translator()
    # 启动 Gradio 服务
    launch_gradio()