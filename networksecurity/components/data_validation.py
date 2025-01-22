from networksecurity.entity.artifact_entity import(
    DataIngestionArtifact,
    DataValidationArtifact
)
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception import NetworkSecurityException
from networksecurity.constant.traning_pipeline import SCHEMA_FILE_PATH
from networksecurity.logging import create_logger
import os, sys
import pandas as pd
from scipy.stats import ks_2samp
from networksecurity.utils.commons import read_yaml_file, write_yaml_file
logger = create_logger(__name__)

class DataValidation:
    def __init__(self,
                 data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig,
                 schema_file_path:str=SCHEMA_FILE_PATH):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.schema_config = read_yaml_file(schema_file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())

    @staticmethod
    def read_data(file_path:str)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())

    def validate_number_of_columns(self, dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns = len(dataframe.columns.tolist())
            if number_of_columns == len(self.schema_config['columns']):
                logger.info(f"Number of columns matched. {number_of_columns} == {len(self.schema_config['columns'])}")
                return True
            logger.info(f"Number of columns not matched. {number_of_columns} != {len(self.schema_config['columns'])}")
            return False
        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())

    def is_numerical_column_exist(self, dataframe:pd.DataFrame)->bool:
        try:
            numerical_columns = list(self.schema_config['numerical_columns'])
            # logger.debug(f"Expected columns are:\n[{numerical_columns}]")
            dataframe_columns = dataframe.columns.tolist()
            # logger.debug(f"Dataframe having:\n[{dataframe_columns}]")
            numerical_columns_present = [column for column in numerical_columns if column in dataframe_columns]
            if len(numerical_columns_present) == len(numerical_columns):
                logger.info(f"All numerical columns present.")
                return True
            logger.info(f"Missing numerical columns. Expected {len(numerical_columns)} columns found {len(numerical_columns_present)}")
            return False
        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())


    def detect_dataset_drift(self, base_df:pd.DataFrame, current_df:pd.DataFrame, threshold:float=0.05)->bool:
        try:
            status = True
            report = {}
            for column in base_df.columns.to_list():
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1, d2)
                if threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False

                report.update({column: {"is_same_dist": is_found,
                                        "pvalue": is_same_dist.pvalue,
                                        'drift_status': is_found}})
            drift_report_file_path = self.data_validation_config.drift_report_file_path

            os.makedirs(os.path.dirname(drift_report_file_path), exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,
                            contents=report, replace=True)
            return status
        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())

    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # read the data from csv file
            train_df = DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)

            # validate the number of columns
            status = self.validate_number_of_columns(dataframe=train_df)
            if not status:
                raise Exception("Train dataframe does not contain all columns")
            status = self.validate_number_of_columns(dataframe=test_df)
            if not status:
                raise Exception("Test dataframe does not contain all columns")

            # validate the numerical columns
            status = self.is_numerical_column_exist(dataframe=train_df)
            if not status:
                raise Exception("Train dataframe does not contain all numerical columns")
            status = self.is_numerical_column_exist(dataframe=test_df)
            if not status:
                raise Exception("Test dataframe does not contain all numerical columns")

            status = self.detect_dataset_drift(base_df=train_df, current_df=test_df)

            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_df.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)
            test_df.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True)


            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path="",
                invalid_test_file_path="",
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())