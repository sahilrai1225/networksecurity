from networksecurity.components.data_ingestion import DataIngestion # class
from networksecurity.components.data_validation import DataValidation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
## to run DataIngestion we need to give DataIngestionConfig as it has patameter 
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from bson import son
import sys


if __name__=="__main__":
    try:
        trainingpiplelineconfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpiplelineconfig)
        dataingestion=DataIngestion(dataingestionconfig)
        logging.info("Initiate the data ingestion") 
        dataingestionartifact=dataingestion.intiate_data_ingestion()
        logging.info("Data initiation completed")
        print(dataingestionartifact)
        datavalidationconfig=DataValidationConfig(trainingpiplelineconfig)
        data_validation=DataValidation(dataingestionartifact,datavalidationconfig)
        logging.info("Initiate the data validation")
        data_validation_artifact=data_validation.initiate_data_validation() 
        logging.info("Data Validation Completed")
        
        print(data_validation_artifact)
    except Exception as e:
        raise NetworkSecurityException(e,sys)        
