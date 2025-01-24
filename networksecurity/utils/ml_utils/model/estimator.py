import os
import sys
import numpy as np
from networksecurity.exception import NetworkSecurityException
from networksecurity.logging import create_logger
from networksecurity.constant.traning_pipeline import SAVE_MODEL_DIR, MODEL_FILE_NAME

logger = create_logger(__name__)

class NetworkSecurityModel:
    def __init__(self, preprocessor:object, model:object):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())

    def predict(self, X:np.array)->np.array:
        try:
            X_transformed = self.preprocessor.transform(X)
            return self.model.predict(X_transformed)
        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())
