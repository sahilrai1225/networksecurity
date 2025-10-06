import logging
import os
from datetime import datetime

## it also important to do logging.config
## Log file name
LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_S')}.log" # strftime is for timestamp
## LOG file path
logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE)
os.makedirs(logs_path,exist_ok=True)

## this is our total path ,path and what file we basically want to create
LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)


# this is basic  info that is required
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO, ## beacuse we ant to keep all the inof
)