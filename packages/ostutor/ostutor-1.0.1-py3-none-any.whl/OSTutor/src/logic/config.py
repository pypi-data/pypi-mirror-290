import os
import json

class Config:
    """
    Config class for managing configuration files.
    """
    data = {}
    def __init__(self):
        self.config_path = os.path.join(os.path.expanduser("~"), ".config", "ostutor", "config.json")
        self.bashrc_path = os.path.join(os.path.expanduser("~"), ".bashrc")
        config_dir = os.path.dirname(self.config_path)
        # 初始化配置文件，如果不存在
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        if not os.path.exists(self.config_path):
            with open(self.config_path, 'w') as config_file:
                json.dump(self.data, config_file, indent=4)
            return
        # 加载配置文件
        self.data = self.load()
    
    # 保存配置
    def save(self): 
        with open(self.config_path, 'w') as config_file:
            json.dump(self.data, config_file, indent=4)
    # 加载配置
    def load(self):
        with open(self.config_path, 'r') as config_file:
            config = json.load(config_file)
            self.data = config
        return self.data
    
    
    # 获取配置
    def get(self, key):
        return self.data.get(key)
    
    # 更新配置
    def update(self, key, value):
        self.data[key] = value
        self.save()
    # 添加配置
    def add(self, key, value):
        self.data[key] = value
        self.save()
    # 删除配置
    def remove(self, key):
        if key in self.data:
            del self.data[key]
            self.save()

    def checkBashrc(self):
        with open(self.bashrc_path, 'r') as bashrc_file:
            self.barshrc = bashrc_file.read()
            if 'shopt -s histappend' not in self.barshrc or 'PROMPT_COMMAND="history -a"' not in self.barshrc:
                return False
        return True
    
    def addHistoryCfgToBashrc(self):
        with open(self.bashrc_path, 'a+') as bashrc_file:
            if 'shopt -s histappend' not in self.barshrc :
                bashrc_file.write('\nshopt -s histappend\n')
            if 'PROMPT_COMMAND="history -a"' not in self.barshrc:
                bashrc_file.write('\nPROMPT_COMMAND="history -a"\n')

        os.system('exec $SHELL')
    
# 实例化配置类
cfg = Config()