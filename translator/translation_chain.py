import os

from langchain.chains.llm import LLMChain
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain_openai import ChatOpenAI

from utils.logger import LOG


class TranslationChain:
    def __init__(self,model_name:str='gpt-3.5-turbo',verbose: bool=True):

        # 翻译任务指令始终由 System角色承担
        with open('translator/prompts/sys_prompt.txt','r',encoding='utf-8') as f:
            template = f.read()

        sys_prompt = SystemMessagePromptTemplate.from_template(template=template)
        human_prompt=HumanMessagePromptTemplate.from_template(template='{inputs}')

        chat_prompt=ChatPromptTemplate.from_messages([
            sys_prompt,human_prompt
        ])

        # 声明一个 OpenAI LLM
        chat_model = ChatOpenAI(
            model_name = model_name,
            api_key=os.getenv('YI_API_KEY'),
            base_url="https://vip.apiyi.com/v1",
            verbose=verbose,
            temperature = 0
        )

        self.chain = LLMChain(llm=chat_model,prompt=chat_prompt,verbose=verbose)

    def invoke(self,inputs:str,source_language:str,target_language:str) ->(str,bool):
        result = ""
        try:
            chain_result = self.chain.invoke({
                'inputs':inputs,
                'source_language':source_language,
                'target_language':target_language
            })
            result = chain_result['text']

        except Exception as e:
            LOG.error(f"An error occurred during translation:{e}")
            return result,False
        return result,True