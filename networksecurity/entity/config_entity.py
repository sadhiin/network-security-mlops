import os
from datetime import datetime

from networksecurity.constant import traning_pipeline

# print(traning_pipeline.PIPELINE_NAME)
# print(traning_pipeline.ARTIFACT_DIR)

class TrainingPipelineConfig:

    def __init__(self) -> None:
        self.timestemp = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
        self.pipeline_name = traning_pipeline.PIPELINE_NAME
        self.artifact_name = traning_pipeline.ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifact_name, self.timestemp)


class DataIngestionConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        self.data_ingestion_dir:str = os.path.join(
            training_pipeline_config.artifact_dir,
            traning_pipeline.DATA_INGESTION_INGESTED_DIR_NAME)

        self.feature_store_file_path:str = os.path.join(
            self.data_ingestion_dir,
            traning_pipeline.DATA_INGESTION_FEATURE_STORE_NAME, traning_pipeline.FEATURE_STORE_FILE_NAME)

        self.train_file_path:str = os.path.join(
            self.data_ingestion_dir,
            traning_pipeline.DATA_INGESTION_INGESTED_DIR_NAME, traning_pipeline.TRAIN_FILE_NAME)

        self.test_file_path:str = os.path.join(
            self.data_ingestion_dir,
            traning_pipeline.DATA_INGESTION_INGESTED_DIR_NAME, traning_pipeline.TEST_FILE_NAME)


        self.train_test_split_ratio:float = traning_pipeline.DATA_INGESTION_SPLIT_RATION
        self.collection_name:str = traning_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name:str = traning_pipeline.DATA_INGESTION_DATABASE_NAME


