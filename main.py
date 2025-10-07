from networksecurity.components.data_ingestion import DataIngestion # class
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
## to run DataIngestion we need to give DataIngestionConfig as it has patameter 
from networksecurity.entity.config_entity import DataIngestionConfig
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
        
        print(dataingestionartifact)
    except Exception as e:
        raise NetworkSecurityException(e,sys)        
