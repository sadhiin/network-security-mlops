
import os
import sys
import json
import numpy as np
import pandas as pd
from networksecurity.logging import create_logger
from networksecurity.exception import NetworkSecurityException
import certifi
from pymongo.mongo_client import MongoClient

from dotenv import load_dotenv
ca = certifi.where()
load_dotenv()
uri = os.getenv('MONGO_DB_URL')
logger = create_logger()
class NetworkDataExtract:
    def __init__(self, file_path):
        try:
            self._csv_to_json_convertor(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())


    def _csv_to_json_convertor(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            self.records = list(json.loads(data.T.to_json()).values())

        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())


    def insert_data_to_mongodb(self, database_name, collection_name):
        try:
            assert uri is not None, 'MongoDB URI is none'
            self.mongo_client = MongoClient(uri)
            self.database = self.mongo_client[database_name]
            self.collection = self.database[collection_name]

            self.collection.insert_many(self.records)
            return len(self.records)
        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())


if __name__=="__main__":
    file_path = r'data\Phishing_Legitimate_full.csv'
    DATABASE = "SADHIN"
    COLLECTION = "NetworkData"

    network_obj = NetworkDataExtract(file_path)

    # num_of_records = network_obj.insert_data_to_mongodb(database_name=DATABASE, collection_name=COLLECTION)
    num_of_records = 10
    logger.info(f"{num_of_records} data insrted to the mongodb database.")
