import sys
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception import NetworkSecurityException
from networksecurity.logging import create_logger
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

logger = create_logger(name="my_logger", filename="my_logger.log")

def main():
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

        logger.debug(f"Data ingestion artifact: {data_ingestion_artifact}")
    except Exception as e:
        raise NetworkSecurityException(e, error_details=sys.exc_info())

if __name__ == "__main__":
    main()


