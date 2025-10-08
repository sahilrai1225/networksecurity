from networksecurity.components.data_ingestion import DataIngestion # class
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_tranformation import DataTransformation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
## to run DataIngestion we need to give DataIngestionConfig as it has patameter 
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTranformationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from bson import son
import sys


if __name__=="__main__":
    try:
        ## for any thing we need to initialize config part first
        trainingpiplelineconfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpiplelineconfig)
        data_ingestion=DataIngestion(dataingestionconfig)
        logging.info("Initiate the data ingestion") 
        data_ingestion_artifact=data_ingestion.intiate_data_ingestion()
        logging.info("Data initiation completed")
        print(data_ingestion_artifact)
        
        datavalidationconfig=DataValidationConfig(trainingpiplelineconfig)
        data_validation=DataValidation(data_ingestion_artifact,datavalidationconfig)
        logging.info("Initiate the data validation")
        data_validation_artifact=data_validation.initiate_data_validation() 
        logging.info("Data Validation Completed")
        print(data_validation_artifact)
        
        logging.info("Initiate the data transformation")
        # concept can be diff but pipleine is same
        datatransformationconfig=DataTranformationConfig(trainingpiplelineconfig)  # from here it will run
        data_transformation=DataTransformation(data_validation_artifact,datatransformationconfig)
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        logging.info("Data Transformation Completed")
        print(data_transformation_artifact)
        
        
    except Exception as e:
        raise NetworkSecurityException(e,sys)        
