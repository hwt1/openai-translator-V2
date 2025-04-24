import time
from typing import Optional

import openai
from openai import OpenAI

from model.model import Model
from utils.config_loader import configYaml
from utils.logger import LOG


class OpenAIModel(Model):
    def __init__(self,model:str,api_key:Optional[str]=None,base_url:Optional[str]=None):
        self.model = model
        if  api_key and base_url:
            self.api_key = api_key
            self.base_url = base_url
        else:
            self.api_key = configYaml['OpenAIModel']['api_key']
            self.base_url = configYaml['OpenAIModel']['base_url']
        self.client = OpenAI(
            api_key = self.api_key,
            base_url = self.base_url
        )

    # 向大模型发起请求
    def make_request(self, prompt):
        attempts = 0
        while attempts < 3 :
            try:
                response = self.client.chat.completions.create(
                    model = self.model,
                    messages=[
                        {"role":"user","content":prompt}
                    ],
                    max_tokens=1000,
                    temperature=0.2
                )
                translation = response.choices[0].message.content.strip()
                print(f"翻译结果为：\n{translation}")
                return translation,True
            except openai.RateLimitError as e:
                attempts += 1
                if attempts < 3:
                    LOG.warning("Rate limit reached.Waiting for 60 seconds before trying.")
                    time.sleep(60)
                else:
                    raise Exception("Rate limit reached.Maximum attempts exceeded.")
            except openai.APIConnectionError as e:
                print("The server could not be reached")
                print(e.__cause__)
                break
            except openai.APIStatusError as e:
                print("Another non-200-range status code was received")
                print(e.status_code)
                print(e.response)
                break
            except Exception as e:
                raise Exception(f"发生了未知错误：{e}")
        return "",False