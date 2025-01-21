import os, sys
import numpy as np
import pandas as pd

TERGET_COLUMN:str = "CLASS_LABEL"
PIPELINE_NAME:str = 'NetworkSecurity'
ARTIFACT_DIR:str = "Artifacts"
FILE_NAME:str = "Phishing_Legitimate_full.csv"

TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"
FEATURE_STORE_FILE_NAME:str = "feature_store.csv"

DATA_INGESTION_DATABASE_NAME:str ="SADHIN"
DATA_INGESTION_COLLECTION_NAME:str = "NetworkData"
DATA_INGESTION_DIR_NAME:str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_NAME:str = "feature_store"
DATA_INGESTION_INGESTED_DIR_NAME:str = "ingested"
DATA_INGESTION_SPLIT_RATION:float = 0.2
