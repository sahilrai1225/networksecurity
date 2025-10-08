from networksecurity.entity.artifacts_entity import DataIngestionArtifact,DataValidationArtifact ## input for this
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file
## scipy for checking data drift
from scipy.stats import ks_2samp
import pandas as pd
import numpy as np

## to validate no of cols or check numnerical col exist or not, we need to define schema and  schema path and based on this we will compare
## how many feild are their or not
## and its code will be in training pipleine which contain schemma file path
## in data validation we need to read that schema and it is imporatnt an compare that schema
## Comapre will be based on schema itself and if it is true it will be col are no mising in df's(train/test)

import os,sys

## input  to data validation is dataingestion artifacts

class DataValidation:
    ## basic init
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)  # to schema.yaml file
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
        
    def validate_number_of_columns(self,dataframe:pd.DataFrame) -> bool:
        try:
            number_of_columns=len(self._schema_config)
            logging.info(f"Required number of column :{number_of_columns}") ## from schema how many col
            logging.info(f"DataFrame has columns :{len(dataframe.columns)}") ## from dataFrame How many col
            
            if len(dataframe.columns)==number_of_columns:
                return True
            else:
                return False
            ## This is validate number of columns 
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def numerical_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            # Select only numeric columns
            num_cols = dataframe.select_dtypes(include=['int64', 'float64']).columns.tolist()
            logging.info(f"Numeric columns: {num_cols}")

            # Return True if any numeric column exists
            return len(num_cols) > 0

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
        
    def detect_dataset_drift(self,base_df,current_df,threshold=0.05)->bool:
        ## confidenece interval
        
        try:
            status=True
            report={}
            for column in base_df.columns: # refernce 
                d1=base_df[column]
                d2=current_df[column]
                
                is_same_dist=ks_2samp(d1,d2) ## Compare dist of 2 sample
                if threshold<=is_same_dist.pvalue:     #dist =distance in is_samole_dist
                    is_found=False
                    
                else:
                    is_found=True
                    status=False  ## condisering change  in dist
                ## if data drift will be there it will create report
                report.update({
                    column:{
                        "p_value":float(is_same_dist.pvalue),
                        "drift_satus":is_found
                    }
                })
                    
            drift_report_file_path=self.data_validation_config.drift_report_file_path
            
            
            ## Create dir
            dir_path=os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report)
            
            ## we neeed to write entire repost in yaml file # to do that write ymal .utils
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
        ## to intiate we need train an test data (output of data ingestion-data ingestion artifact) and from data ingestion component 
    def initiate_data_validation(self) ->DataIngestionArtifact: ## telling that its output will be datavalidationartifact
        try:
            train_file_path=self.data_ingestion_artifact.trained_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path
            
            # read the data from train and test
            train_dataframe=DataValidation.read_data(train_file_path)
            test_dataframe=DataValidation.read_data(test_file_path)
            
            
            #  Validate Number of columns
            ## And validating with help of schema
            
            status=self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:   ## status not true means false
                error_message=f"Train DataFrame does not contain all columns .\n"
            
            status=self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:   ## status not true means false
                error_message=f"Test DataFrame does not contain all columns .\n"
            
            ## Checking whether numerical columns exist or not  do yourself
            status=self.numerical_columns(dataframe=train_dataframe)
            if not status:   ## status not true means false
                error_message=f"Train DataFrame does not contain numericla columns.\n"
            
            status=self.numerical_columns(dataframe=test_dataframe)
            if not status:   ## status not true means false
                error_message=f"Test DataFrame does not contain numerical columns .\n"          
                
            ## Lets check data drift 
            status=self.detect_dataset_drift(base_df=train_dataframe,current_df=test_dataframe)
            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path) ## status if true then our dataset should go in valid_train_file 
            os.makedirs(dir_path,exist_ok=True)
            
            ## if status is true we don't need to worry and there is no  isse
            
            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path,index=False,header=True
            )
            
            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path,index=False,header=True
            )
            ## we donot usse status here as main thing is down below
            
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,  ## here we used status 
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )
            return data_validation_artifact     
            
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)




