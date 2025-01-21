import os
import sys
import pandas as pd
import numpy as np
from pymongo.mongo_client import MongoClient
import certifi
from typing import List
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv

# configuration of the data ingestion config
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.exception import NetworkSecurityException
from networksecurity.logging import create_logger

load_dotenv()
MONGO_DB_URL = os.getenv('MONGO_DB_URL')
logger = create_logger()

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())


    def _export_collection_as_dataframe(self):
        """
            export the collection data as a dataframe
        """
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = MongoClient(MONGO_DB_URL)
            data = pd.DataFrame(list(self.mongo_client[database_name][collection_name].find()))

            if '_id' in data.columns.to_list():
                data.drop(columns=['_id'], axis=1, inplace=True)

            data.replace({'na':np.nan}, inplace=True)

            return data
        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())

    def export_data_into_feature_store(self, dataframe:pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.makedirs(os.path.dirname(feature_store_file_path), exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False, header=True)

            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())

    def split_data_as_train_test(self, dataframe:pd.DataFrame, random_state:int=42):
        try:
            train_set, test_set = train_test_split(dataframe,
                                                   test_size=self.data_ingestion_config.train_test_split_ratio,
                                                   shuffle=True,
                                                   random_state=random_state)
            logger.info(f"splitting data into train and test")
            dir_path = os.makedirs(os.path.dirname(self.data_ingestion_config.train_file_path), exist_ok=True)
            logger.info(f"Saving the train and test file in the directory {dir_path}")

            train_set.to_csv(self.data_ingestion_config.train_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.test_file_path, index=False, header=True)
        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())

    def initiate_data_ingestion(self):
        try:
            dataframe = self._export_collection_as_dataframe()
            self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)

            data_ingestion_artifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.train_file_path,
                                                            test_file_path=self.data_ingestion_config.test_file_path)
            logger.info(f"Data ingestion is completed successfully")
            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e, error_details=sys.exc_info())
    