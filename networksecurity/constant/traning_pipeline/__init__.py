import os, sys
import numpy as np
import pandas as pd

TARGET_COLUMN:str = "CLASS_LABEL"
PIPELINE_NAME:str = 'NetworkSecurity'
ARTIFACT_DIR:str = "artifacts"
FILE_NAME:str = "Phishing_Legitimate_full.csv"

TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"
FEATURE_STORE_FILE_NAME:str = "feature_store.csv"

SCHEMA_FILE_PATH:str = os.path.join("data_schema", "schema.yaml")

DATA_INGESTION_DATABASE_NAME:str ="SADHIN"
DATA_INGESTION_COLLECTION_NAME:str = "NetworkData"
DATA_INGESTION_DIR_NAME:str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_NAME:str = "feature_store"
DATA_INGESTION_INGESTED_DIR_NAME:str = "ingested"
DATA_INGESTION_SPLIT_RATION:float = 0.2

DATA_VALIDATION_DIR_NAME:str = "data_validation"
DATA_VALIDATION_VALID_DIR:str = "validated"
DATA_VALIDATION_INVALID_DIR:str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR:str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str = "drift_report.yaml"

DATA_TRANSFORMATION_DIR_NAME:str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR:str = "transformed"
TRANSFORMED_OBJECT_FILE_NAME:str = "transformed_object.pkl"
## knn imputer parameters
DATA_TRANSFORMATION_IMPUTER_PARMS:dict = {
    'missing_values':np.nan,
    'n_neighbors':5,
    'weights':'uniform'
}

