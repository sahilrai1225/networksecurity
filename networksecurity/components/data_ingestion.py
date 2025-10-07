from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

## Confguration of the Data ingestion Cofig

from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifacts_entity import DataIngestionArtifact ## output of datainestion compoeemts

import os
import sys
import numpy as np
import pandas as pd
import pymongo
from typing import List
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv() ## env variavle

MONGO_DB_URL=os.getenv("MONGO_DB_URL")


## when we do Data ingestion it should know all detail of Data ingestion confi
class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config  ## This will have all acees to what we created in data ingestion config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
        
        
    ## from mongodb collection impoart data as dataframe   and initiaeing config
    def export_collection_as_dataframe(self):
        
        
        """
       READ DATA FROM MONGODB
        """
        try:
            database_name=self.data_ingestion_config.database_name ## In data _ingestion_config here databse name is present
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL) ## MongoClient will helpful in creating client itself
            collection=self.mongo_client[database_name][collection_name]
            
            df=pd.DataFrame(list(collection.find()))
            # whenever we will read data from Mongodb, one additional col get created that is id
            if "_id" in df.columns.to_list():
                df=df.drop(columns=["_id"],axis=1)
                
                
            df.replace({"na":np.nan},inplace=True)
            return df
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
        
    ## storing in files    
            
    def export_data_into_feature_store(self,dataframe: pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path  ## Availabe in constant 
            #creating folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)  ## iN feature_stor_file_path our dat will bw stored in that as csv
            return dataframe
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def split_data_as_train_test(self,dataframe: pd.DataFrame):
        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Performed train test split on the dataframe")

            logging.info(
                "Exited split_data_as_train_test method of Data_Ingestion class"
            )
            ## to save it in file path 
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            
            os.makedirs(dir_path, exist_ok=True)
            
            logging.info(f"Exporting train and test file path.")
            
            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )

            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )
            logging.info(f"Exported train and test file path.")
            
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
   
    ## 2nd step in pdf is to intiate Data Ingestion config  
    def intiate_data_ingestion(self):
        try:
            ## to intiate data_ingestion_config we need to have df and reading mongo df data
            dataframe=self.export_collection_as_dataframe()
            dataframe=self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            dataingestionartifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                         test_file_path=self.data_ingestion_config.testing_file_path)
            
            return dataingestionartifact
            ## This is final output of dataingestion components
        except Exception as e:
            raise NetworkSecurityException(e,sys) 
        
        
        ## Once we read data from mongodb we donot nedd to read again and agian from  mongodb we save them in .csv file
        
        
    ## Train tets split after creating folder