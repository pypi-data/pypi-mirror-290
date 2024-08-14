from abc import ABC, abstractmethod

class AbstractAnalysis(ABC):
    @abstractmethod
    def run_analysis(self, data):
        """执行数据分析"""
        pass

    @abstractmethod
    def get_results(self):
        """返回分析结果"""
        pass

class PCAAnalysis(AbstractAnalysis):
    def __init__(self):
        self.results = None

    def run_analysis(self, data):
        from sklearn.decomposition import PCA
        pca = PCA(n_components=2)
        self.results = pca.fit_transform(data)

    def get_results(self):
        return self.results