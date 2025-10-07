import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os
import sys
# import dill
import pickle


## Creating a function read_yaml_file for data validation , it is genric

def read_yaml_file(file_path:str) ->dict: # shoould return value in form of dict 
    try: #beacuse we are reading it from schema and it is there in key-value pair
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
        
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)  ## it will just write content in that 
    except Exception as e:
        raise NetworkSecurityException(e, sys)