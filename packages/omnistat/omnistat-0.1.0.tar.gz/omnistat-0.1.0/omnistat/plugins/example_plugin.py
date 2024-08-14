from abc import ABC, abstractmethod

class AbstractPlugin(ABC):
    @abstractmethod
    def register(self):
        """插件注册方法"""
        pass

    @abstractmethod
    def execute(self, *args, **kwargs):
        """插件执行方法"""
        pass

class ExamplePlugin(AbstractPlugin):
    def register(self):
        print("Example plugin registered.")

    def execute(self, *args, **kwargs):
        print("Executing example plugin with arguments:", args, kwargs)