import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.entity.artifacts_entity import (
    DataTransformationArtifact,DataValidationArtifact
)
## data Tranformation artofact is final o/p of data_transformationn 
## Data Transformation in depend upon data validtion outputs


from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import DataTranformationConfig
from networksecurity.utils.main_utils.utils import save_numpy_array_data,save_object # this both will be used in tthis file

class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTranformationConfig):
        try:
            self.data_validation_artifact:DataValidationArtifact=data_validation_artifact  ## These are the thing we required intially
            self.data_transformation_config:DataTranformationConfig=data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
         ## as it is init func so in main pipepline we will give these 2 paar which require
         
    @staticmethod # to read datframe of test /train
    def read_data(file_path) ->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
        
    # function to intializw KNN
    def get_data_tranformer__object(cls) ->Pipeline : # type is pipeline andt this piple is what we imported from sklearn.pipleine
        """
        It  intialize a KNNImputer object with the parameter specified in the training_pipeline.py file
        and returns a Pipeline object with the KNNImputer object as the first step

        Args:
            cls:DataTransformation
        Returns:
            A Pipeline Object
        And all ourcode will be in pipeline
        """
        logging.info("Entered get data_tranformer_object method of Tranformation data")
        try:
            imputer:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)  # specifiy return type as KNN Inmputer
            ## ** beacuse in key value pair
            logging.info(f"Initialize KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}")
            
            processor:Pipeline=Pipeline([("imputer",imputer)])
            
            return processor
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_data_transformation(self)->DataTransformationArtifact:
        ## return output for it
        logging.info("Entered initiate_data_tranformatiob method of DataTransformation class")
        try:
            logging.info("Starting data tranformation")
            # reading train and test data for that we will use static method s in
            # st method we donot need to initialize any obj we can directly use with classname
            ## data _validation artifact is output of data validationn
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
           
            # after getting train and test df frame we need to apply KNN imputer before that remove target var
           
            ## training df ## need to remve result ## creating independt and dep 
            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df=train_df[TARGET_COLUMN]
            
            ## by seeing result it is classification problem and we need to convert o/p from 1,-1 to 1,0
            target_feature_train_df=target_feature_train_df.replace(-1,0)
            
            
            ## testing dataframe
            input_feature_test_df=test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df=test_df[TARGET_COLUMN]
            target_feature_test_df=target_feature_test_df.replace(-1,0)
            
            ## completed reading Train and test data
            ## Implementing KNN imputer for that we will call data_tranformmer obj
            preprocessor=self.get_data_tranformer__object() # calling a function inside a claa
            
            preprocessor_object=preprocessor.fit(input_feature_train_df)
            tranformed_input_train_feature=preprocessor_object.transform(input_feature_train_df)
            tranformed_input_test_feature=preprocessor_object.transform(input_feature_test_df)
            # for test data we need to just apply tranfrom
            
            # these both will be an array so we will combine as array
            # c_ just combine tranformed input array into target arr
            train_arr=np.c_[tranformed_input_train_feature,np.array(target_feature_train_df)]
            test_arr=np.c_[tranformed_input_test_feature,np.array(target_feature_test_df)]
            
            
            # calling save function to save our np arrray in spec ific folder
            
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,array=train_arr,)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array=test_arr,)
            # numpy array will be saved in tranformed_train/test_file_path folder
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor_object,)
            
            
            ## save pkl file in final_model 
            
            save_object("final_model/preprocessor.pkl",preprocessor_object)
            ## save object is getting called from utils.py which ahve this function to save pkl file
            
            ## Preparing Artifacts
            ## they are output which will be passed on model _trainer
            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            
            
            return data_transformation_artifact
            
            
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)