import os
import sys
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_trasnformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.entity.config_entity import(
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig
)
from networksecurity.entity.artifact_entity import(
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact
)

from networksecurity.exception import NetworkSecurityException
from networksecurity.logging import create_logger


logger = create_logger(__name__)

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

    def start_data_ingestion(self):
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logger.info("Data Ingestion started")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logger.info(f"Data Ingestion completed: {data_ingestion_artifact}")
            return data_ingestion_artifact            
        except Exception as e:
            logger.error(f"Error in training pipeline: {str(e)}")
            raise NetworkSecurityException(e, sys.exc_info())
        
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact)->DataValidationArtifact:
        try:
            self.data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            logger.info("Data Validation started")
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=self.data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            logger.info(f"Data Validation completed: {data_validation_artifact}")
            return data_validation_artifact
        
        except Exception as e:
            logger.error(f"Error in data validation: {str(e)}")
            raise NetworkSecurityException(e, sys.exc_info())
        
    def start_data_transformation(self, data_validation_artifact: DataValidationArtifact)->DataTransformationArtifact:
        try:
            self.data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            logger.info("Data Transformation started")
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,
                data_transformation_config=self.data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logger.info(f"Data Transformation completed: {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            logger.error(f"Error in data transformation: {str(e)}")
            raise NetworkSecurityException(e, sys.exc_info())
        
    def start_model_train(self, data_transformation_artifact: DataTransformationArtifact)->ModelTrainerArtifact:
        try:
            self.model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            logger.info("Model Training started")
            model_trainer = ModelTrainer(model_trainer_config=self.model_trainer_config,
                                         data_transformation_artifact=data_transformation_artifact)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logger.info(f"Model Training completed: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            logger.error(f"Error in model training: {str(e)}")
            raise NetworkSecurityException(e, sys.exc_info())
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            data_trasnformation_artifact = self.start_data_transformation(data_validation_artifact)
            model_trainer_artifact = self.start_model_train(data_trasnformation_artifact)
            return model_trainer_artifact
        except Exception as e:
            logger.error(f"Error in running pipeline: {str(e)}")
            raise NetworkSecurityException(e, sys.exc_info())