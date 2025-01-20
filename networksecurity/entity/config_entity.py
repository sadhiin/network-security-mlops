import os
from datetime import datetime

from networksecurity.constant import traning_pipeline

print(traning_pipeline.PIPELINE_NAME)
print(traning_pipeline.ARTIFACT_DIR)

class TrainingPipelineConfig:

    def __init__(self) -> None:
        self.timestemp = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
        self.pipeline_name = traning_pipeline.PIPELINE_NAME
        self.artifact_name = traning_pipeline.ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifact_dir, self.timestemp)


class DataIngestionConfig:
    def __init__(self, training_pipeline_config = TrainingPipelineConfig):
        self.data_ingestion_dir:str = os.path.join(
            training_pipeline_config.artifact_dir,
            traning_pipeline.DATA_INGESTION_INGESTED_DIR_NAME)


