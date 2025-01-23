import sys
from networksecurity.exception import NetworkSecurityException
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_trasnformation import DataTransformation
from networksecurity.entity.config_entity import (
    DataIngestionConfig,
    TrainingPipelineConfig,
    DataValidationConfig,
    DataTransformationConfig)

from networksecurity.logging import create_logger

logger = create_logger(name="my_logger", filename="my_logger.log")

def main():
    try:
        logger.info(f"Starting the data ingestion step")
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        # logger.debug(f"Data ingestion artifact: {data_ingestion_artifact}")

        logger.info(f"Starting the Datavalidation step")
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(
            data_ingestion_artifact=data_ingestion_artifact,
            data_validation_config= data_validation_config,
        )

        data_validation_artifact= data_validation.initiate_data_validation()
        logger.info(f"Initiate the data validaton")
        # print(data_validation_artifact)

        logger.info(f"Starting the data trasformations steps.")
        data_transformation_confg = DataTransformationConfig(training_pipeline_config)
        data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,
                                                 data_transformation_config=data_transformation_confg)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)

    except Exception as e:
        raise NetworkSecurityException(e, error_details=sys.exc_info())

if __name__ == "__main__":
    main()


