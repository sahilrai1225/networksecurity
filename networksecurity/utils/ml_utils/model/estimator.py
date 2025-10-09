## the reason to create this file is to create Network data model
## so  we can return prepocessing pkl and model pkl

## we will  save processed pkl (from Data  Transfornation )file and model file


from networksecurity.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME

import os
import sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


class NetworkModel:
    ## initailziation of both preprocessor and model
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def predict(self,x):
        try:
            x_transform = self.preprocessor.transform(x) ## tranform on newdata
            y_hat = self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise NetworkSecurityException(e,sys)
