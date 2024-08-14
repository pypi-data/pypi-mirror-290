from abc import ABC, abstractmethod

class AbstractDataLoader(ABC):
    @abstractmethod
    def load_data(self, source):
        """从给定的源加载数据"""
        pass

    @abstractmethod
    def preprocess_data(self, data):
        """对加载的数据进行预处理"""
        pass

class CSVDataLoader(AbstractDataLoader):
    def load_data(self, source):
        import pandas as pd
        return pd.read_csv(source)

    def preprocess_data(self, data):
        # 实现具体的预处理逻辑
        return data.dropna()