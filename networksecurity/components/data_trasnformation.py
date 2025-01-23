import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline


from networksecurity.constant.traning_pipeline import TARGET_COLUMN, DATA_TRANSFORMATION_IMPUTER_PARMS
from networksecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact
)
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.exception import NetworkSecurityException
from networksecurity.logging import create_logger
from networksecurity.utils.commons import save_object, save_numpy_array_data

logger = create_logger(__name__)


class DataTransformation:
    def __init__(self, data_transformation_config:DataTransformationConfig,
                 data_validation_artifact:DataValidationArtifact):
        try:
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())

    @staticmethod
    def read_data(file_path:str)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())


    def get_data_transformer_object(self)->Pipeline:
        try:
            logger.info(f"{'>>'*20} Strating the data transformer object {'<<'*20}")

            knn_imputer_model = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARMS)
            logger.info(f"{'>>'*20} KNN Imputer model loaded with parameters: {DATA_TRANSFORMATION_IMPUTER_PARMS} parameters {'<<'*20}")

            pipeline_processor = Pipeline([
                ('imputer', knn_imputer_model)
            ])

            return pipeline_processordill
        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())

    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            logger.info(f"{'>>'*20} Data Transformation starting {'<<'*20}")
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            # training dataframe
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]

            # testing dataframe
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]

            pre_processor_object = self.get_data_transformer_object()
            pre_processor_object.fit(input_feature_train_df)

            transformed_train_arr = pre_processor_object.transform(input_feature_train_df)
            transformed_test_arr = pre_processor_object.transform(input_feature_test_df)

            train_arr = np.c_[transformed_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_test_arr, np.array(target_feature_test_df)]

            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, test_arr)

            save_object(self.data_transformation_config.transformed_object_file_path, pre_processor_object)
            # prepare datatransform artifaces
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )

            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())

