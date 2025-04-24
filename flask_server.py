import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, send_file, jsonify

from translator.pdf_translator import PDFTranslator
from translator.translation_config import TranslationConfig
from utils.argument_parser import ArgumentParser
from utils.logger import LOG

app=Flask(__name__)

TEMP_FILE_DIR = 'flask_temps/'

@app.route('/translation',methods=['POST'])
def translation():
    try:
        input_file = request.files['input_file']
        source_language = request.form.get('source_language')
        target_language = request.form.get('target_language')
        output_file_format = request.form.get('output_file_format')

        LOG.debug(f"[input_file]\n{input_file}")
        LOG.debug(f"[input_file.filename]\n{input_file.filename}")

        if input_file and input_file.filename:
            # 创建临时文件
            input_file_path = TEMP_FILE_DIR+input_file.filename
            LOG.debug(f"[input_file_path]\n{input_file_path}")

            input_file.save(input_file_path)

            # 调用翻译函数
            output_file_path = Translator.translate_pdf(
                input_file=input_file_path,
                source_language=source_language,
                target_language=target_language,
                output_file_format=output_file_format
            )

            # 移除临时文件
            os.remove(input_file_path)

            # 构造完整路径
            output_file_path = os.getcwd()+'/'+output_file_path
            LOG.debug(f'翻译后文件完整路径：{output_file_path}')

            # 返回翻译后的文件
            return send_file(output_file_path,as_attachment=True)
    except Exception as e:
        LOG.error(f'/translation 请求异常，{e}')
        response = {
            'status':'error',
            'message':str(e)
        }
        return jsonify(response),400



def initialize_translator():
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()

    config = TranslationConfig()
    config.initialize(args)

    global Translator
    Translator = PDFTranslator(config.model_name)

if __name__ == '__main__':
    initialize_translator()

    # 启动 Flask Web server
    app.run(host='127.0.0.1',port=5000,debug=True)