from abc import ABC, abstractmethod

class AbstractVisualizer(ABC):
    @abstractmethod
    def visualize(self, data, **kwargs):
        """可视化数据"""
        pass

class ScatterPlotVisualizer(AbstractVisualizer):
    def visualize(self, data, **kwargs):
        import matplotlib.pyplot as plt
        plt.scatter(data[:, 0], data[:, 1], **kwargs)
        plt.show()