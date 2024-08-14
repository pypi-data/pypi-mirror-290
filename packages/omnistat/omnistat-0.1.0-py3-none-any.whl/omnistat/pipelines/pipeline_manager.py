from workflows.single_cell.sc_pipeline import SingleCellPipeline
from workflows.transcriptomics.transcript_pipeline import TranscriptomicsPipeline
from workflows.proteomics.proteomics_pipeline import ProteomicsPipeline

class PipelineManager:
    def __init__(self):
        self.pipelines = [
            SingleCellPipeline(),
            TranscriptomicsPipeline(),
            ProteomicsPipeline()
        ]

    def run_all_pipelines(self):
        for pipeline in self.pipelines:
            pipeline.run()