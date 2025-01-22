import os, sys
import yaml
# import dill
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