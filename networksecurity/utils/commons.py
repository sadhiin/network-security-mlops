import os, sys
import yaml
import pickle
import numpy as np
from networksecurity.exception import NetworkSecurityException
from networksecurity.logging import create_logger

logger = create_logger(__name__)

def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise NetworkSecurityException(e, sys.exc_info())

def write_yaml_file(file_path: str, contents:object, replace:bool=True)->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs((os.path.dirname(file_path)), exist_ok=True)
        with open(file_path, 'w') as file:
            yaml.dump(contents, file)
    except Exception as e:
        raise NetworkSecurityException(e, sys.exc_info())


def save_numpy_array_data(file_path:str, array:np.array)->None:
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file:
            np.save(file, array)
    except Exception as e:
        raise NetworkSecurityException(e, sys.exc_info())


def save_object(file_path:str, obj:object)->None:
    try:
        logger.info(f"Saving object at path: {file_path}")
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file:
            pickle.dump(obj, file)
    except Exception as e:
        raise NetworkSecurityException(e, sys.exc_info())

