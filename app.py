import os, sys
import certifi
import pandas as pd
from dotenv import load_dotenv
import pymongo
from networksecurity.exception import NetworkSecurityException
from networksecurity.logging import create_logger
from networksecurity.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from uvicorn import run as app_run
from fastapi.responses import JSONResponse
from fastapi.responses import Response
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from starlette.responses import RedirectResponse

from networksecurity.utils.commons import load_object
from networksecurity.constant.traning_pipeline import DATA_INGESTION_COLLECTION_NAME, DATA_INGESTION_DATABASE_NAME


ca = certifi.where()
load_dotenv()
mongo_uri = os.getenv("MONGO_DB_URL")
client = pymongo.MongoClient(mongo_uri, tlsCAFile=ca)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"] # support all the origin requests

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=['authentication'])
async def index():
    return RedirectResponse(url="/docs")

@app.get('/health', tags=['health'])
async def health():
    return {"status": "UP"}

@app.get('/train')
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful.",status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__=='__main__':
    app_run(app, host='0.0.0.0', port=8000)