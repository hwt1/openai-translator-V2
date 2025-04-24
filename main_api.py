
import os
import sys
import time

from flask import Flask, request, jsonify
from flask_cors import CORS

from model.openai_model import OpenAIModel
from translator.pdf_translator import PDFTranslator
from utils.config_loader import configYaml

# 获取项目根路径的绝对路径
project_root =os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,project_root)

# 封装API方法
app = Flask(__name__)

# 添加跨域处理
CORS(app)

# 定义API路由
# 测试请求
@app.route('/api/data',methods=['get'])
def test_data():
    result = "request success"
    return jsonify({"result":result})

@app.route('/translate',methods=['POST'])
def translate_api():
    # 获取请求中的 JSON数据
    data = request.get_json()

    model_name = data['model_name']
    pdf_file_path = data['pdf_file_path']

    model = OpenAIModel(model=model_name)
    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
    translator = PDFTranslator(model)
    result = translator.translate_pdf(pdf_file_path=pdf_file_path)
    return jsonify({"result":result})

@app.route('/api/translate',methods=['POST'])
def translate_from_page():

    # 获取 modelName
    model_name = request.form.get('modelName') if request.form.get('modelName') else configYaml['OpenAIModel']['model']
    file_format = request.form.get('fileFormat') if request.form.get('fileFormat') else 'PDF'
    target_language = request.form.get('targetLanguage') if request.form.get('targetLanguage') else configYaml['defaultTargetLanguage']

    # 获取上传的文件
    file = request.files.get('file')
    if not file:
        return jsonify({'error':'文件未上传'}),400
    # 检查文件类型
    if file.filename.split('.')[-1].lower() !='pdf':
        return jsonify({'error':'只支持上传 PDF文件'}),400

    save_file_path,ui_file_url=handle_translated_file_path(file.filename,file_format,target_language)

    model = OpenAIModel(model=model_name)
    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
    translator = PDFTranslator(model)
    translator.translate_pdf(pdf_file=file,output_file_path=save_file_path,file_format=file_format,target_language=target_language)


    return jsonify({
        'status': 'success',
        'outFileUrl':ui_file_url
    })

# 处理翻译后文件路径
def handle_translated_file_path(filename:str,file_format:str,target_language:str):
    # 翻译后文件输出路径
    timestamp = str(time.time()).replace(".", "")
    file_suffix = f"_translated_{target_language}_{timestamp}.{'pdf' if file_format.lower() == 'pdf' else 'md'}"
    translated_file_name = f"{filename.replace('.pdf', file_suffix)}"
    # 翻译后文件保存路径
    save_file_path = f"translate-ui/public/translated_files/{translated_file_name}"
    # 拼接前端访问翻译后的文件链接
    ui_base_url = configYaml['UIBaseUrl']
    ui_file_url = f"{ui_base_url}translated_files/{translated_file_name}"
    return save_file_path,ui_file_url
if __name__ == '__main__':
    app.run()