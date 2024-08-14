from abc import ABC, abstractmethod
import json

class AbstractConfigManager(ABC):
    @abstractmethod
    def load_config(self, file_path):
        """加载配置文件"""
        pass

    @abstractmethod
    def get_config(self, key):
        """获取特定配置值"""
        pass

    @abstractmethod
    def set_config(self, key, value):
        """设置特定配置值"""
        pass

class JSONConfigManager(AbstractConfigManager):
    def __init__(self):
        self.config = {}

    def load_config(self, file_path):
        with open(file_path, 'r') as f:
            self.config = json.load(f)

    def get_config(self, key):
        return self.config.get(key)

    def set_config(self, key, value):
        self.config[key] = value