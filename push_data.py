import os
import sys
import json

## to call all env variables here for MGDB URl to know ehre to push data
from dotenv import load_dotenv

load_dotenv()
## To get mongodb url
MONGO_DB_URL=os.getenv("MONGO_DB_URL")

print(MONGO_DB_URL)

## Certifi  - a python package wwhich provide roots certificate ,commonly used by python library to establish secure
## HTTP connect and here we are connecting with mongodb This is to ensure that it trust only this trusted certified
import certifi
ca=certifi.where()  ## this line retrives the part to bundle of ca(certificate authority) certificte provided by certifi
## we will be using this certificate for trust and all

import pandas as pd
import numpy as np
import pymongo
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException


## It is ETL pipleine which is  responsible for
## Read all data and convert into json filr
class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        ## File_path is imoptrant because it give us path from where to read file
    def csv_to_json_convertor(self,file_path):
        try:
            data=pd.read_csv(file_path)
            ## droping index as we donot need this in mongodb
            data.reset_index(drop=True,inplace=True)
            records=list(json.loads(data.T.to_json()).values()) # to convert into array and lisr
            return records
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def insert_data_mongodb(self,records,database,collection):
        try:
            # self.database=database
            # self.collection=collection
            # self.records=records
            
            # ## mongo_client should be intialized with pymongo to connect to mongo db
            # self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            # ## assigning
            # self.database= self.mongo_client[self.database]
            
            # self.collection=self.database[self.collection]
            # self.collection.insert_many(self.records)
            self.database = database
            self.collection = collection
            self.records = records

## Initialize Mongo client
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)

## Assign database and collection
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]

## Insert records
            self.collection.insert_many(self.records)

            
            return (len(self.records))
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
        
## ETL pipelineODE

if __name__=="__main__":
    FILE_PATH="Network_Data/phisingData.csv"
    DATABASE="NETWORK_SECURITY"
    Collection="NetworkData"
    networkobj=NetworkDataExtract() ## Intializing Class above
    records=networkobj.csv_to_json_convertor(file_path=FILE_PATH)
    print(records)
    no_of_records=networkobj.insert_data_mongodb(records,DATABASE,Collection)
    print(no_of_records)