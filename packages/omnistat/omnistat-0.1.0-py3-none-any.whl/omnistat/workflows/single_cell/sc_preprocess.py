from core.preprocess import AbstractPreprocessor

class SingleCellPreprocessor(AbstractPreprocessor):
    def apply(self, data):
        # Implement specific preprocessing for single cell data
        return data