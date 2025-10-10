# import os
# import sys

# from networksecurity.exception.exception import NetworkSecurityException
# from networksecurity.logging.logger import logging

# ## importing all clas
# from networksecurity.components.data_ingestion import DataIngestion
# from networksecurity.components.data_validation import DataValidation
# from networksecurity.components.data_tranformation import DataTransformation
# from networksecurity.components.model_trainer import ModelTrainer

# ## importing all config entity

# from networksecurity.entity.config_entity import (
#     TrainingPipelineConfig,
#     DataIngestionConfig,
#     DataValidationConfig,
#     DataTranformationConfig,
#     ModelTrainerConfig,
# )

# ## importing artifacts entity -- all these require for any stage we go

# from networksecurity.entity.artifacts_entity import (
#     DataIngestionArtifact,
#     DataValidationArtifact,
#     DataTransformationArtifact,
#     ModelTrainerArtifact,
# )

# ## write all code in class form for modular coding
# ## run all config file
# class TrainingPipeline:
#     def __init__(self):
#         self.training_pipeline_config=TrainingPipelineConfig()
#         ## inside training pipeline first step we need to initiate is data ingetion
        
#     def start_data_ingestion(self):
#         try:
#             ## In data ingetsion first thing we required is data_ingestion -config , for data ing we need to give Training pipeline
#             self.data_ingestion_config=DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
#             logging.info("Start Data Ingestion")
            
#             ## creating data ingestion -- intialaize data ingetsion class
#             data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion_config)
#             data_ingestion_artifact=data_ingestion.intiate_data_ingestion()  ## o/p of ini data in is DI artifacts
#             logging.info(f"Data Ingestion Completed and aritfact : {data_ingestion_artifact}")
#             return data_ingestion_artifact
#             ## this artifacts sholud go for next 
#         except Exception as e:
#             raise NetworkSecurityException(e,sys)
        
#     def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact):
#         try:
#             data_validation_config=DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
#             data_validation=DataValidation(data_validation_config=data_validation_config,data_ingestion_artifact=data_ingestion_artifact)
#             logging.info("Initiate Data Validation")
#             data_validation_artifact=data_validation.initiate_data_validation()
            
#             return data_validation_artifact           
        
#         except Exception as e:
#             raise NetworkSecurityException(e,sys)
        
#     def start_data_transformation(self,data_validation_artifact:DataValidationArtifact):
#         try:
#             data_transformation_config=DataTranformationConfig(training_pipeline_config=self.training_pipeline_config)
#             data_transformation=DataTransformation(data_transformation_config=data_transformation_config,
#                                                    data_validation_artifact=data_validation_artifact)
            
#             data_transformation_artifact=data_transformation.initiate_data_transformation()
#             return data_transformation_artifact
        
#         except Exception as e:
#             raise NetworkSecurityException(e,sys)
        
#     def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact):
#         try:
#             model_trainer_config= ModelTrainerConfig(
#                 training_pipeline_config=self.training_pipeline_config
#             )

#             model_trainer = ModelTrainer(
#                 data_transformation_artifact=data_transformation_artifact,
#                 model_trainer_config=model_trainer_config
#             )

#             model_trainer_artifact = model_trainer.initiate_model_trainer()

#             return model_trainer_artifact

#         except Exception as e:
#             raise NetworkSecurityException(e, sys)
        
        
#     def run_pipeline(self): # The best thing about this functio is it will run one by one
#         try:  # for running in pipeline ## this way one bye one we will be able  to execute this
#             data_ingestion_artifact=self.start_data_ingestion()
#             data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
#             data_transformation_artifact=self.start_data_transformation(data_validation_artifact=data_validation_artifact)
#             model_trainer_artifact=self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            
#             return model_trainer_artifact
            
            
#         except Exception as e:
#             raise NetworkSecurityException(e,sys)


import os
import sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

# Importing all components
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_tranformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

# Importing all config entities
from networksecurity.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTranformationConfig,
    ModelTrainerConfig,
)

# Importing all artifact entities
from networksecurity.entity.artifacts_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact,
)

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

    def start_data_ingestion(self):
        try:
            self.data_ingestion_config = DataIngestionConfig(
                training_pipeline_config=self.training_pipeline_config
            )
            logging.info("Starting Data Ingestion")

            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config
            )
            data_ingestion_artifact = data_ingestion.intiate_data_ingestion()
            logging.info(f"Data Ingestion completed: {data_ingestion_artifact}")

            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact):
        try:
            data_validation_config = DataValidationConfig(
                training_pipeline_config=self.training_pipeline_config
            )
            data_validation = DataValidation(
                data_validation_config=data_validation_config,
                data_ingestion_artifact=data_ingestion_artifact,
            )
            logging.info("Initiating Data Validation")

            data_validation_artifact = data_validation.initiate_data_validation()
            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def start_data_transformation(self, data_validation_artifact: DataValidationArtifact):
        try:
            data_transformation_config = DataTranformationConfig(
                training_pipeline_config=self.training_pipeline_config
            )
            data_transformation = DataTransformation(
                data_transformation_config=data_transformation_config,
                data_validation_artifact=data_validation_artifact,
            )

            data_transformation_artifact = data_transformation.initiate_data_transformation()
            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact)->ModelTrainerArtifact:
        try:
            model_trainer_config = ModelTrainerConfig(
                training_pipeline_config=self.training_pipeline_config
            )

            model_trainer = ModelTrainer(
                data_transformation_artifact=data_transformation_artifact,
                model_trainer_config=model_trainer_config,
            )

            model_trainer_artifact = model_trainer.initiate_model_trainer()
            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(
                data_ingestion_artifact=data_ingestion_artifact
            )
            data_transformation_artifact = self.start_data_transformation(
                data_validation_artifact=data_validation_artifact
            )
            model_trainer_artifact = self.start_model_trainer(
                data_transformation_artifact=data_transformation_artifact
            )

            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
