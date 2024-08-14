from pipelines.pipeline_manager import PipelineManager

def main():
    manager = PipelineManager()
    manager.run_all_pipelines()

if __name__ == "__main__":
    main()