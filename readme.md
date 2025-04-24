**一、项目分为几个模块**

1、pdf解析模块——用于获取原文

2、OpenAI模型模块——用于进行翻译

3、prompt提示词模块——用于构造提示词，便于扩展

4、writer输出模块——用于归纳配置内容

5、读取配置文件模块——用于归纳配置内容

6、logger日志模块——用于记录日志


**二、框架说明**

1、Gradio + Flask + LangChain + Argparse命令行解析

**三、OpenAI Translator 项目改造内容：**

1、引入LangChain框架，将LLM请求改为 LangChain方式

2、优化启动方式
* 命令行启动
* API请求
* Gradio图形化界面方式

3、优化日志记录