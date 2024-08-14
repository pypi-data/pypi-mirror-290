from abc import ABC, abstractmethod

class AbstractPreprocessor(ABC):
    @abstractmethod
    def apply(self, data):
        """对数据应用预处理步骤"""
        pass

class NormalizationPreprocessor(AbstractPreprocessor):
    def apply(self, data):
        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler()
        return scaler.fit_transform(data)