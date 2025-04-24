# 用于读取配置文件——yaml文件
import yaml


class ConfigLoader:
    def __init__(self,config_path):
        self.config_path = config_path
    def load_config(self):
        with open(self.config_path,"r",encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config
configYaml = ConfigLoader('config.yaml').load_config()

if __name__ == "__main__":
    config = ConfigLoader("../config.yaml").load_config()
    print(config)
    print(type(config)) # <class 'dict'>

