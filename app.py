## app.py should be frontend
## Create api using fastapi

import sys
import os

import certifi
ca=certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url=os.getenv("MONGO_DB_URL")
print(mongo_db_url)  ## loading this to initiate dataingestion

import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,File,UploadFile,Request
from uvicorn import run as app_run  ## uvicorn to run our app and all
from fastapi.responses import Response
from starlette.responses import RedirectResponse

import pandas as pd
import numpy as np


from networksecurity.utils.main_utils.utils import load_object ## to load pkl file

## to read client mongo
client=pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)

from networksecurity.constant.training_pipeline import (DATA_INGESTION_COLLECTION_NAME,
                                                        DATA_INGESTION_DATABASE_NAME)

## will create a client to load database itself
database=client[DATA_INGESTION_DATABASE_NAME]
collection=client[DATA_INGESTION_COLLECTION_NAME]

## important for creating fastapi -- for accessing in browser
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
## to read template folder in fastapi
from fastapi.templating import Jinja2Templates
templates=Jinja2Templates(directory="./templates")

## get request -- hardcoded thing in fastapi
@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


## to get recent data and ETL pipleine we can run pushdata.py

@app.get("/train") # basic training entire training pipeline ,for that initiatize trainnh pipleine
async def train_route():
    try:
        ## initiate trainingpipleine
        train_pipeline=TrainingPipeline()
        train_pipeline.run_pipeline()  ## for runnning entire pipeline
        
        return Response("Training is Succesful")
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
## from input data we need to do prediction

@app.post("/predict")
async def predict_route(request: Request,file: UploadFile = File(...)): ## uploading test.csv for prediction
    try:
        df=pd.read_csv(file.file)
        #print(df)
        preprocesor=load_object("final_model/preprocessor.pkl")
        ## these 2 for batch prediction 
        final_model=load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocesor,model=final_model)
        print(df.iloc[0])
        y_pred = network_model.predict(df)
        print(y_pred)
        df['predicted_column'] = y_pred
        print(df['predicted_column'])
        #df['predicted_column'].replace(-1, 0)
        #return df.to_json()
        df.to_csv('prediction_output/output.csv') ## in this our o/p values will be ## can be in any mongo db ,html., ...
        table_html = df.to_html(classes='table table-striped') ## in table.html 
        #print(table_html)
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
        
    except Exception as e:
            raise NetworkSecurityException(e,sys)

    

if __name__=="__main__" : ## giving entry point to run this
    app_run(app,host="localhost",port=8000)  # given ;ocal host but when deploy give 0.0.0.0
